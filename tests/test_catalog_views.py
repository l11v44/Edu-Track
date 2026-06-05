import pytest
from django.urls import reverse
from tests.factories import CourseFactory, UserFactory, LessonFactory


@pytest.mark.django_db
def test_course_list_view(client):
    user = UserFactory()
    CourseFactory(status='Published', author=user)
    client.force_login(user)

    url = reverse('course_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'courses' in response.context


@pytest.mark.django_db
def test_course_detail_view(client):
    user = UserFactory()
    course = CourseFactory(status='Published')
    course.students.add(user)

    client.force_login(user)
    url = reverse('course_detail', kwargs={'slug': course.slug})

    response = client.get(url)
    assert response.status_code == 200
    assert response.context['course'] == course


@pytest.mark.django_db
def test_enroll_in_course_view(client):
    user = UserFactory()
    course = CourseFactory(status='Published')

    client.force_login(user)
    url = reverse('enroll_in_course', kwargs={'slug': course.slug})

    response = client.post(url)

    assert response.status_code == 302
    assert course.students.filter(id=user.id).exists()