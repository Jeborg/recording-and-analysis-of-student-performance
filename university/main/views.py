from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q, Avg
from django.db import connection
from openpyxl import Workbook
from .models import *
from .forms import *
from .filters import *



@login_required 
def home(request):
    # Проверка на группу пользователя
    is_student = request.user.groups.filter(name='students').exists()
    is_professor = request.user.groups.filter(name='professors').exists()

    context = {"is_student": is_student, "is_professor": is_professor}

    return render (request, 'main/index.html', context)


def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect ("main:login")
    else:
        form = UserCreationForm()

    return (request, "registration/signup.html", {"form": form})


def studentDebt(request):
    is_student = request.user.groups.filter(name='students').exists()
    # Получаем активный id пользователя из таблицы auth_user
    current_user = request.user
    current_user_id = current_user.id
    
    # Кастомный запрос из БД для активного студента
    cursor = connection.cursor()
    cursor.execute("SELECT subjects.subject_name, subjects.course, scores.date, scores.value, scores.type FROM scores JOIN students ON scores.student_id = students.id JOIN subjects ON scores.subject_id = subjects.id WHERE students.user_id = %s AND (scores.value = 2 OR scores.value IS NULL)", [current_user_id])
    debt = cursor.fetchall()

    return render (request, "main/debt.html", {"debt" : debt, "is_student": is_student})


def studentAcademicPerformance(request):
    is_student = request.user.groups.filter(name='students').exists()
    # Получаем активный id пользователя из таблицы auth_user
    current_user = request.user
    

    subject = request.GET.get('subject_name', '')
    course = request.GET.get('course', '')
    type = request.GET.get('type', '')

    scores = Score.objects.select_related('student', 'subject').order_by('subject__subject_name', '-subject__course', 'type')
    scores = scores.filter(student__user=current_user)

    if subject:
        scores = scores.filter(subject__subject_name__icontains=subject)
    if course:
        scores = scores.filter(subject__course=course)
    if type:
        scores = scores.filter(type__icontains=type)
    # Преобразование данных в удобный формат
    scores_data = [
        {
            'subject_name': score.subject.subject_name,
            'course': score.subject.course,
            'date': score.date,
            'value': score.value,
            'type': score.type,
        }
        for score in scores
    ]

    context = {"is_student": is_student, "scores_data": scores_data}

    return render (request, "main/studentAcademicPerformance.html", context)


def averageGradeBySubject(request):
    is_student = request.user.groups.filter(name='students').exists()
    # Получаем активный id пользователя из таблицы auth_user
    current_user = request.user
    


    aver_grade = Score.objects.select_related('subject').values('subject__subject_name', 'subject__course') \
                              .annotate(average_grade=Avg('value'))
    aver_grade = aver_grade.filter(student__user=current_user)

    # Преобразование данных в удобный формат
    aver_grade_data = [
        {
            'subject_name': grade['subject__subject_name'],
            'course': grade['subject__course'],
            'average_grade': grade['average_grade'],
        }
        for grade in aver_grade
    ]

    context = {"is_student": is_student, "aver_grade": aver_grade_data}

    return render (request, "main/average_grade_by_subject.html", context)


def averageGradeByCourse(request):
    is_student = request.user.groups.filter(name='students').exists()
    # Получаем активный id пользователя из таблицы auth_user
    current_user = request.user
    


    aver_grade = Score.objects.select_related('subject').values('subject__course') \
                              .annotate(average_grade=Avg('value')) \
                              .order_by('subject__course')
    aver_grade = aver_grade.filter(student__user=current_user)

    # Преобразование данных в удобный формат
    aver_grade_data = [
        {
           'course': grade['subject__course'],
           'average_grade': grade['average_grade'],
        }
        for grade in aver_grade
    ]

    context = {"is_student": is_student, "aver_grade": aver_grade_data}

    return render (request, "main/average_grade_by_course.html", context)


def totalAverageGrade(request):
    is_student = request.user.groups.filter(name='students').exists()
    # Получаем активный id пользователя из таблицы auth_user
    current_user = request.user
    

    total_average_grade = Score.objects.select_related('subject') \
                                       .filter(student__user=current_user) \
                                       .aggregate(total_average_grade=Avg('value'))['total_average_grade']


    context = {"is_student": is_student, "total_average_grade": total_average_grade}

    return render (request, "main/total_average_grade.html", context)


def studentsAverageGradeByGroup(request):
    # Получаем активный id пользователя из таблицы auth_user
    current_user = request.user
    
     # Проверка, что текущий пользователь является преподавателем
    is_professor = request.user.groups.filter(name='professors').exists()
    if not Professor.objects.filter(user=current_user).exists():
        return render(request, 'main/students_average_grade_by_group.html', {'error': 'Вы не являетесь преподавателем.'})

    studentsAverGrade = Score.objects.select_related('subject', 'student__group_set') \
                          .filter(subject__teacher__user=current_user) \
                          .values('subject__subject_name', 'student__group__group_name') \
                          .annotate(average_grade=Avg('value')) \
                          .order_by('student__group__group_name', 'subject__subject_name')

    studentsAverGrade_data = [
        {
            'subject_name': grade['subject__subject_name'],
            'group_name': grade['student__group__group_name'],
            'average_grade': grade['average_grade'],
        }
        for grade in studentsAverGrade
    ]

    context = {"is_professor": is_professor, "studentsAverGrade": studentsAverGrade_data}

    return render (request, "main/students_average_grade_by_group.html", context)


def exportStudentsAverageGradeByGroup(request):
    current_user = request.user
    
    # Проверка, что текущий пользователь является преподавателем
    if not Professor.objects.filter(user=current_user).exists():
        return HttpResponse('Вы не являетесь преподавателем.', status=403)

    studentsAverGrade = Score.objects.select_related('subject', 'student__group_set') \
                          .filter(subject__teacher__user=current_user) \
                          .values('subject__subject_name', 'student__group__group_name') \
                          .annotate(average_grade=Avg('value')) \
                          .order_by('student__group__group_name', 'subject__subject_name')

    # Создание Excel файла
    wb = Workbook()
    ws = wb.active
    ws.title = "Средний балл по группе"

    # Запись заголовков
    ws.append(['Предмет', 'Группа', 'Средний балл'])

    # Запись данных
    for grade in studentsAverGrade:
        ws.append([
            grade['subject__subject_name'],
            grade['student__group__group_name'],
            round(grade['average_grade'], 2)
        ])

    # Настройка ответа
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=students_average_grade_by_group.xlsx'
    wb.save(response)

    return response


def Profile(request):
    current_user = request.user
    current_user_id = current_user.id

    # Проверка на группу пользователя
    is_student = request.user.groups.filter(name='students').exists()
    is_professor = request.user.groups.filter(name='professors').exists()
    
    # Запрос к БД для вытягывания данных об активном студенте
    cursor1 = connection.cursor()
    cursor1.execute("SELECT students.last_name, students.first_name, students.middle_name, students.email, groups.group_name, roles.name, MAX(subjects.course) AS current_course FROM students LEFT JOIN groups ON students.id = groups.student_id LEFT JOIN roles ON students.role_id = roles.id LEFT JOIN scores ON students.id = scores.student_id JOIN subjects ON scores.subject_id = subjects.id WHERE students.user_id = %s GROUP BY students.last_name, students.first_name, students.middle_name, students.email, groups.group_name, roles.name", [current_user_id])
    student_info = cursor1.fetchall()

    # Запрос к БД для вытягывания данных об активном преподавателе
    cursor2 = connection.cursor()
    cursor2.execute("SELECT professors.last_name, professors.first_name, professors.middle_name, professors.email, roles.name, string_agg(subjects.subject_name, ', ') FROM professors LEFT JOIN roles ON professors.role_id = roles.id JOIN subjects ON professors.id = subjects.teacher_id WHERE professors.user_id = %s GROUP BY professors.last_name, professors.first_name, professors.middle_name, professors.email, roles.name", [current_user_id])
    professor_info = cursor2.fetchall()

    context = {"student_info": student_info, "professor_info": professor_info, "is_student": is_student, "is_professor": is_professor}

    return render (request, "main/profile.html", context)


@csrf_protect
def professor_control(request):
    # Проверка на группу пользователя
    is_professor = request.user.groups.filter(name='professors').exists()

    current_user = request.user

    group_name = request.GET.get('group_name', '')
    subject_name = request.GET.get('subject_name', '')
    course = request.GET.get('course', '')
    type = request.GET.get('type', '')

    # Получаем все необходимые данные, используя select_related и prefetch_related для оптимизации запросов
    scores = Score.objects.select_related('student', 'subject').prefetch_related('subject__teacher', 'student__group_set')

    if group_name:
        scores = scores.filter(student__group__group_name__icontains=group_name)
    if subject_name:
        scores = scores.filter(subject__subject_name__icontains=subject_name)
    if course:
        scores = scores.filter(subject__course=course)
    if type:
        scores = scores.filter(type__icontains=type)
    
    # Фильтруем по профессору
    scores = scores.filter(subject__teacher__user=current_user)

    academicPerformance = [
        {
            'student_id': score.student.id, 
            'last_name': score.student.last_name, 
            'first_name': score.student.first_name, 
            'middle_name': score.student.middle_name, 
            'group_id': score.student.group_set.first().id, 
            'group_name': score.student.group_set.first().group_name, 
            'subject_id': score.subject.id, 
            'subject_name': score.subject.subject_name, 
            'course': score.subject.course, 
            'score_id': score.id, 
            'date': score.date, 
            'type': score.type, 
            'value': score.value
        }
        for score in scores
    ]

    context = {"academicPerformance": academicPerformance, "is_professor": is_professor}
    return render(request, 'main/professor_control.html', context)


@csrf_protect
def update_academic_performance(request):
    if request.method == 'POST':
        data = request.POST
        student_ids = data.getlist('student_id')
        last_names = data.getlist('last_name')
        first_names = data.getlist('first_name')
        middle_names = data.getlist('middle_name')
        group_ids = data.getlist('group_id')
        group_names = data.getlist('group_name')
        subject_ids = data.getlist('subject_id')
        subject_names = data.getlist('subject_name')
        courses = data.getlist('course')
        score_ids = data.getlist('score_id')
        dates = data.getlist('date')
        types = data.getlist('type')
        values = data.getlist('value')

        for i in range(len(student_ids)):
            print(f"Processing record {i + 1}/{len(student_ids)}")  # Debug output
            student_id = student_ids[i]
            last_name = last_names[i]
            first_name = first_names[i]
            middle_name = middle_names[i]
            group_id = group_ids[i]
            group_name = group_names[i]
            subject_id = subject_ids[i]
            subject_name = subject_names[i]
            course = courses[i]
            score_id = score_ids[i]
            date = dates[i]
            type_ = types[i]
            value = values[i]

            if not date:
                continue  # Пропустить запись, если дата отсутствует или пуста

            # Обновление студента
            if student_id:
                student = Student.objects.get(id=student_id)
                student.last_name = last_name
                student.first_name = first_name
                student.middle_name = middle_name
                student.save()

            # Обновление группы
            if group_id:
                group = Group.objects.get(id=group_id)
                group.group_name = group_name
                group.save()

            # Обновление предмета
            if subject_id:
                subject = Subject.objects.get(id=subject_id)
                subject.subject_name = subject_name
                subject.course = course
                subject.save()

            # Обновление оценки
            if score_id:
                score = Score.objects.get(id=score_id)
                score.date = date
                score.type = type_
                score.value = value
                score.save()
            else:
                Score.objects.create(
                    student_id=student_id,
                    subject_id=subject_id,
                    date=date,
                    type=type_,
                    value=value
                )

    return redirect('professor_control')
