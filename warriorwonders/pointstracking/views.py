from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Student, Teacher, School
from django.db.models import Prefetch
from django.views.generic import DetailView, ListView


class IndexView(ListView):
    model = School
    template_name = 'pointstracking/index.html'
    context_object_name = 'schools_list'
    
    def get_queryset(self):
        return School.objects.all().prefetch_related(
            Prefetch('teachers', queryset=Teacher.objects.order_by('grade__sort_order'))
        )

class TeacherView(DetailView):
    model = Teacher
    template_name = 'pointstracking/teacher.html'
    context_object_name = 'teacher'
