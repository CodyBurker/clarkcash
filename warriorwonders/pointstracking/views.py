from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Student, Teacher, School


def index(request):
    schools = School.objects.all()
    context = {'schools_list': schools}
    return render(request, 'pointstracking/index.html', context)

def student(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
        # Create simple response with student string
        return_string = str(student)
        return HttpResponse(return_string)
    
    except Student.DoesNotExist:
        raise Http404("Student does not exist")

def school(request, school_id):
    try:
        school = School.objects.get(pk=school_id)
        # Create simple response with school string
        return_string = str(school)
        return HttpResponse(return_string)
    
    except School.DoesNotExist:
        raise Http404("School does not exist")

def teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(pk = teacher_id)
        # Template teacher.html
        return render(request, 'pointstracking/teacher.html', {'teacher': teacher}) 
    except Teacher.DoesNotExist:
        raise Http404("Teacher does not exist")