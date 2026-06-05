import pytest
from catalog.models import Course
from .factories import CourseFactory, UserFactory
from django.db import models

@pytest.mark.django_db
def test_popular_courses_aggregation():
    course1 = CourseFactory()
    course2 = CourseFactory()
    student = UserFactory()

    course1.students.add(student)

    popular = Course.objects.annotate(num_students=models.Count('students')).order_by('-num_students')

    assert popular[0].num_students == 1
    assert popular[1].num_students == 0