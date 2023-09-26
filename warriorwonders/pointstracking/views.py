from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Student, Teacher, School
from django.db.models import Prefetch
from django.views.generic import DetailView, ListView, FormView
from .forms import UpdatePointsForm

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

class UpdateStudentPointsView(FormView):
    template_name = 'pointstracking/update_points.html'
    def post(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm(request.POST)
        if form.is_valid():
            points = form.cleaned_data['points']
            student.add_points(points)
            return redirect('pointstracking:index')

# def update_student_points(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
    
#     if request.method == 'POST':
#         form = UpdatePointsForm(request.POST)
#         if form.is_valid():
#             points = form.cleaned_data['points']
#             student.add_points(points)
#             return redirect('pointstracking:index')
#     else:
#         form = UpdatePointsForm()

#     context = {'form': form, 'student': student}
#     return render(request, 'pointstracking/update_points.html', context)