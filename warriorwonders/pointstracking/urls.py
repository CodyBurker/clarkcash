from django.urls import path

from . import views
app_name = 'pointstracking'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('students/<int:student_id>/', views.student, name='student'),
    # path('schools/<int:school_id>/', views.school, name='school'),
    path('teachers/<int:pk>/', views.TeacherView.as_view(), name='teacher'),
    path('update_points/<int:student_id>/', views.UpdateStudentPointsView.as_view(), name='update_points'),
    path('spend_points/<int:student_id>/', views.SpendPointsView.as_view(), name='spend_points'),
    path('schools/<int:pk>/', views.SchoolView.as_view(), name='schools'),
]