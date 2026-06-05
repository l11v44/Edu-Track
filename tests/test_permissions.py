import pytest
from django.urls import reverse
from rest_framework import status
from tests.factories import UserFactory

@pytest.mark.skip(reason="")
@pytest.mark.django_db
def test_student_cannot_delete_other_submission(client):
    owner = UserFactory()
    stranger = UserFactory()

    client.force_login(stranger)

    # Предположим, у тебя есть URL для удаления задания
    url = reverse('submission-delete', kwargs={'pk': 1})
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN