from .models import Grade, School
def grades(request):     
    return {'grades': Grade.objects.all()}

def schools(request):
    return {'schools': School.objects.all()}