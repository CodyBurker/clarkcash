from django.urls import path

from . import views
app_name = 'pointstracking'
urlpatterns = [
    path('', views.index, name='index'),
    path('students/<int:student_id>/', views.student, name='student'),
    path('schools/<int:school_id>/', views.school, name='school'),
    path('teachers/<int:teacher_id>/', views.teacher, name='teacher'),
]