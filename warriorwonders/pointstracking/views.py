from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, Http404
from .models import Student, Teacher, School, Grade, QuickSpendPoint
from django.db.models import Prefetch
from django.views.generic import DetailView, ListView, FormView
from .forms import UpdatePointsForm
from django.contrib import messages
from django.views.generic.base import ContextMixin
from rest_framework.views import APIView
from rest_framework.response import Response
import polars as pl

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

class SpendPointsView(FormView, ContextMixin):
    template_name = 'pointstracking/spend_points.html'

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     student_id = self.kwargs.get('student_id')
    #     student = get_object_or_404(Student, id=student_id)
    #     quickspendpoints = QuickSpendPoint.objects.all()
    #     # context['student'] = student
    #     # context['quick_spend_points'] = quickspendpoints
    #     print(quickspendpoints)
    #     return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm(request.POST)
        if form.is_valid():
            points = form.cleaned_data['points']
            if points <= 0:
                messages.error(request, 'Must be a positive amount of Clark Cash')
                return redirect('pointstracking:spend_points', student_id=student_id)
            student.redeem_points(points)
            messages.success(request, f'Successfully redeemed {points} points for {student.name}')
            return redirect('pointstracking:schools', pk = student.teacher.school.id)
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm()
        context = {
            'form': form, 
            'student': student, 
            'quick_spend_points': QuickSpendPoint.objects.order_by('points').all()
            }
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
            user = request.user.get_username()
            student.add_points(points, user)
            messages.success(request, f'Successfully added {points} points for {student.name}')
            return redirect('pointstracking:schools', pk = student.teacher.school.id)
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm()
        context = {'form': form, 'student': student}
        return render(request, self.template_name, context)

class SpendStudentPointsView(FormView, ContextMixin):
    template_name = 'pointstracking/update_points.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data()
        context['quick_spend'] = QuickSpendPoint.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm(request.POST)
        if form.is_valid():
            points = form.cleaned_data['points']
            user = request.user.get_username()
            student.redeem_points(points, user)
            return redirect('pointstracking:school')
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = UpdatePointsForm()
        context = {'form': form, 'student': student}
        return render(request, self.template_name, context)

class SchoolView(DetailView):
    model = School
    template_name = 'pointstracking/school.html'
    context_object_name = 'school'
    # Add extra context to the view
    # Add list of grades in addition to school object
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        school_id = self.kwargs.get('pk')
        school = get_object_or_404(School, id=school_id)
        context['school'] = school
        sorted_grades = Grade.objects.order_by('sort_order').all()
        context['grades'] = sorted_grades
        return context

class StudentView(DetailView):
    model = Student
    template_name = 'pointstracking/student.html'
    context_object_name = 'student'

# Get data for chart.js
# Of student points over time
class StudentChartData(APIView):
    def get(self, request, format=None, **kwargs):
        student_id = self.kwargs.get('pk')
        student = get_object_or_404(Student, id=student_id)
        points = student.point_set.all()
        labels = []
        data = []
        # Use polars to group points by month and sum
        df = pl.DataFrame(
            {'date': [point.date for point in points],
             'value': [point.value for point in points]}
        ).with_columns(date = pl.col('date').cast(pl.Date),
                       value = pl.col('value').cast(pl.Int64)
        ).with_columns(month = pl.col('date').dt.month()
        ).groupby('month').agg(pl.sum('value').alias('value'))
        labels = df['month'].to_list()
        data = df['value'].to_list()
        # for point in points:
        #     labels.append(point.date.strftime('%m/%d/%Y'))
        #     data.append(point.value)
        return Response(data={
            'labels': labels,
            'chartData': data,
        })