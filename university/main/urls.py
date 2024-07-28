from django.urls import path, include
from . import views
from .views import authView

urlpatterns = [
     path("", views.home, name='home'),
     path("signup/", authView, name="authView"),
     path("accounts/", include("django.contrib.auth.urls")),

     path("debt/", views.studentDebt, name="debt" ),
     path("profile/", views.Profile, name="profile"),
     path("control/", views.professor_control, name="control"),
     path('update_academic_performance/', views.update_academic_performance, name='update_academic_performance'),
     path("studentAcademicPerformance/", views.studentAcademicPerformance, name="studentAcademicPerformance"),
     path("averageGradeBySubject/", views.averageGradeBySubject, name="averageGradeBySubject"),
     path("averageGradeByCourse/", views.averageGradeByCourse, name="averageGradeByCourse"),
     path("totalAverageGrade/", views.totalAverageGrade, name="totalAverageGrade"),
     path("studentsAverageGradeByGroup/", views.studentsAverageGradeByGroup, name="studentsAverageGradeByGroup"),
     path("exportStudentsAverageGradeByGroup", views.exportStudentsAverageGradeByGroup, name="exportStudentsAverageGradeByGroup")
]