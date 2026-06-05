import factory
from main.models import User
from catalog.models import Course

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Faker('email')


import factory
from catalog.models import Course


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Sequence(lambda n: f"Course {n}")
    slug = factory.Sequence(lambda n: f"course-{n}")


class LessonFactory:
    pass