from django.db import models
from django.utils import timezone

class School(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Grade(models.Model):
    name = models.CharField(max_length=50)
    sort_order = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    def __str__(self):
        return f'{self.name} - {self.grade} @ {self.school}'

class Student(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        grade = self.teacher.grade
        return f'{self.name} - {self.teacher}'

    def check_points(self):
        points = Point.objects.filter(student=self)
        total = 0
        for point in points:
            total += point.value
        return total
    
    def redeem_points(self, value):
        available_points = self.check_points()
        if value <= available_points:
            # Create point object with negative value of points to redeem
            point = Point(student=self, 
                          value=-value, 
                          date=timezone.now(),
                          description="Redeemed points"
                          )
            point.save()
            return True
        else:
            # Redeem all of students points
            point = Point(
                student=self, 
                value=-available_points, 
                date=timezone.now(),
                description="Redeemed points (all points)"
                )
            point.save()
            return True
    def add_points(self, vaue: int):
        point = Point(
            student=self, 
            value=vaue, 
            date=timezone.now(),
            description="Added points"
            )
        point.save()
        return True

class Point(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField('date')
    value = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.student} - ({self.value}) - {self.date} - {self.description}'