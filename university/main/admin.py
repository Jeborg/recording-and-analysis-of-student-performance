from django.contrib import admin
from .models import *

# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    # Поля для отображения
    list_display = ('id', 'name')
    # Поля для поиска
    search_fields = ('id', 'name')

class StudentAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'last_name', 'first_name', 'middle_name', 'email', 'role')
    search_fields = ('id', 'last_name', 'first_name', 'middle_name')

class ProfessorAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'last_name', 'first_name', 'middle_name', 'email', 'role')
    search_fields = ('id', 'last_name', 'first_name', 'middle_name')

class SubjectAdmin(admin.ModelAdmin):
    
    def teacher_name (self,obj):
        return obj.teacher
    
    def teach_id (self,obj):
        return obj.teacher_id
    
    teacher_name.short_description = 'Преподаватель'
    teach_id.short_description = 'ID Преподавателя'

    list_display = ('id', 'subject_name', 'teacher_name', 'teach_id', 'course')
    search_fields = ('id', 'subject_name', 'teacher', 'teacher_id', 'course')

class GroupAdmin(admin.ModelAdmin):

    def professor (self,obj):
        if obj.subject.teacher.middle_name == None:
            return f"{obj.subject.teacher.last_name} {obj.subject.teacher.first_name}"
        else:
            return f"{obj.subject.teacher.last_name} {obj.subject.teacher.first_name} {obj.subject.teacher.middle_name}"
    
    professor.short_description = 'Преподаватель'

    list_display = ('id', 'group_name', 'subject', 'student', 'professor')
    search_fields = ('id', 'group_name')

class ScoreAdmin(admin.ModelAdmin):

    list_display = ('id', 'student', 'subject', 'date', 'value', 'type')
    search_fields = ('id', 'student', 'subject')



admin.site.register(Role, RoleAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Score, ScoreAdmin)