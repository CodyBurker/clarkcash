from django.contrib import admin

# Register your models here.
from .models import School, Grade, Teacher, Student, Point, QuickSpendPoint

admin.site.register(School)
admin.site.register(Grade)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Point)
admin.site.register(QuickSpendPoint)