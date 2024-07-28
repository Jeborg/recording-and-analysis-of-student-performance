from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.db import models
from django.conf import settings

# Create your models here.


class Role(models.Model):
    """Роли"""

    class Meta:
        db_table = "roles"
        verbose_name = "роль"
        verbose_name_plural = "Роли"

    role_status = (
        ('студент', 'студент'),
        ('преподаватель', 'преподаватель'),
        ('администратор', 'администратор')
    )

    name = models.CharField (choices=role_status, verbose_name="Роль")

    def __str__(self):
        return self.name
    

class Student(models.Model):
    """Студенты"""

    class Meta:
        db_table = "students"
        verbose_name = "студента"
        verbose_name_plural = "Информация о студентах"

    last_name = models.CharField (max_length=30, blank=False, verbose_name="Фамилия")
    first_name = models.CharField (max_length=30, blank=False, verbose_name="Имя")
    middle_name = models.CharField (max_length=30, blank=True, null=True, verbose_name="Отчество")
    email = models.EmailField (blank=False, verbose_name="E-mail")
    role = models.ForeignKey (Role, default=1, on_delete=models.CASCADE, verbose_name="Роль")
    user = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    


class Professor(models.Model):
    """Преподаватели"""

    class Meta:
        db_table = "professors"
        verbose_name = "преподавателя"
        verbose_name_plural = "Информация о преподавателях"

    last_name = models.CharField (max_length=30, blank=False, verbose_name="Фамилия")
    first_name = models.CharField (max_length=30, blank=False, verbose_name="Имя")
    middle_name = models.CharField (max_length=30, blank=True, null=True, verbose_name="Отчество")
    email = models.EmailField (blank=False, verbose_name="E-mail")
    role = models.ForeignKey (Role, default=2, on_delete=models.CASCADE, verbose_name="Роль")
    user = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    

class Subject(models.Model):
    """Предметы"""

    class Meta:
        db_table = "subjects"
        verbose_name = "дисциплину"
        verbose_name_plural = "Дисциплины"

    subject_name = models.CharField (max_length=100, blank=False, verbose_name="Дисциплина")
    course = models.IntegerField (blank=False, default=1, verbose_name="Курс")
    teacher = models.ForeignKey (Professor, on_delete=models.CASCADE, verbose_name="ID преподавателя")

    def __str__(self):
        return f"{self.subject_name}, Курс: {self.course}"
    

class Group(models.Model):
    """Группы"""

    class Meta:
        db_table = "groups"
        verbose_name = "группу"
        verbose_name_plural = "Группы"

    group_name = models.CharField (max_length=20, blank=False, verbose_name="Группа")
    subject = models.ForeignKey (Subject, on_delete=models.CASCADE, null=True, verbose_name="ID предмета")
    student = models.ForeignKey (Student, on_delete=models.RESTRICT, null=True, verbose_name="ID студента")

    def __str__(self):
        return self.group_name
    
    
class Score(models.Model):
    """Оценки"""

    class Meta:
        db_table = "scores"
        verbose_name = "оценки"
        verbose_name_plural = "Оценки"

    type_choices = (
        ('Тест', 'Тест'),
        ('Экзамен', 'Экзамен'),
        ('Зачет', 'Зачет'),
        ('Курсовая работа', 'Курсовая работа'),
        ('Лабораторная работа', 'Лабораторная работа'),
        ('Посещаемость', 'Посещаемость')
    )    

    student = models.ForeignKey (Student, on_delete=models.CASCADE, blank=False, verbose_name="ID студента")
    subject = models.ForeignKey (Subject, on_delete=models.CASCADE, blank=False, verbose_name="ID предмета")
    date = models.DateField (verbose_name="Дата")
    value = models.IntegerField (blank=True, null=True, verbose_name="Балл")
    type = models.CharField (blank=True, choices=type_choices, verbose_name="Тип оценивания")

    def __str__(self):
        return f"{self.student_id} {self.subject_id} {self.date} {self.type} {self.value}"