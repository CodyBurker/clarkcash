from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, Http404
from .models import Student, Teacher, School
from django.db.models import Prefetch
from django.views.generic import DetailView, ListView, FormView
from .forms import UpdatePointsForm
from django.contrib import messages

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

class SpendPointsView(FormView):
    template_name = 'pointstracking/spend_points.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        context['student'] = student
        return context
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm(request.POST)
        if form.is_valid():
            points = form.cleaned_data['points']
            student.redeem_points(points)
            messages.success(request, f'Successfully redeemed {points} points for {student.name}')
            return redirect('pointstracking:index')
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm()
        context = {'form': form, 'student': student}
        return render(request, self.template_name, context)

class UpdateStudentPointsView(FormView):
    template_name = 'pointstracking/update_points.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        context['student'] = student
        return context
    
    def post(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm(request.POST)
        if form.is_valid():
            points = form.cleaned_data['points']
            student.add_points(points)
            messages.success(request, f'Successfully added {points} points for {student.name}')
            return redirect('pointstracking:index')
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm()
        context = {'form': form, 'student': student}
        return render(request, self.template_name, context)

class SpendStudentPointsView(FormView):
    # use same template as UpdateStudentPointsView
    template_name = 'pointstracking/update_points.html'
    def post(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm(request.POST)
        if form.is_valid():
            points = form.cleaned_data['points']
            student.redeem_points(points)
            return redirect('pointstracking:index')
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm()
        context = {'form': form, 'student': student}
        return render(request, self.template_name, context)