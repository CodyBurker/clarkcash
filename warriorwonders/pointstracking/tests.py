from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from .models import Student, Teacher, School, Grade

# Helper function to setup

def setup_helper(calling_object):
    school = School.objects.create(name='Test School')
    grade = Grade.objects.create(name='Test Grade', sort_order=1)
    teacher = Teacher.objects.create(name='Test Teacher', school=school, grade=grade)
    student = Student.objects.create(name='Test Student', teacher=teacher)
    student2 = Student.objects.create(name='Test Student 2', teacher=teacher)
    calling_object.school = school
    calling_object.grade = grade
    calling_object.teacher = teacher
    calling_object.student = student
    calling_object.student2 = student2

class StudentModelTests(TestCase):
    def setUp(self):
        setup_helper(self)
    def test_add_points(self):
        self.student.add_points(10)
        student_points = self.student.check_points()
        self.assertEqual(student_points, 10)
    def test_redeem_points(self):
        self.student.add_points(10)
        self.student.redeem_points(5)
        student_points = self.student.check_points()
        self.assertEqual(student_points, 5)

class IndexViewTest(TestCase):
    def test_index_view_with_no_students(self):
        response = self.client.get(reverse('pointstracking:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No schools available.')
        self.assertQuerysetEqual(response.context['schools_list'], [])
    def test_index_view_with_students(self):
        setup_helper(self)
        response = self.client.get(reverse('pointstracking:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test School')
        self.assertContains(response, 'Test Grade')
        self.assertContains(response, 'Test Teacher')
        self.assertContains(response, 'Test Student')

class UpdatePointsFormTest(TestCase):
    def setUp(self):
        setup_helper(self)
    def test_update_points_form(self):
        response = self.client.get(reverse('pointstracking:update_points', args=(self.student.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Student')

class SchoolViewTest(TestCase):
    def setUp(self):
        setup_helper(self)

    def test_school_view(self):
        url = reverse('pointstracking:schools', args=(self.school.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test School')
        self.assertContains(response, 'Test Teacher')
        self.assertContains(response, 'Test Student')
        self.assertContains(response, 'Test Student 2')
        self.assertTemplateUsed(response, 'pointstracking/school.html')