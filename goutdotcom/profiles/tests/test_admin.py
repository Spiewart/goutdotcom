import pytest
from django.urls import reverse

from goutdotcom.users.models import User
from goutdotcom.profiles.models import PatientProfile

pytestmark = pytest.mark.django_db

class TestPatientProfileAdmin:
        def test_add(self, admin_client):
            url = reverse("admin:profiles_patientprofile_add")
            response = admin_client.get(url)
            assert response.status_code == 200

            response = admin_client.post(
                url,
                data={
                    "user": "testuser",
                    "picture": "My_R@ndom-P@ssw0rd",
                },
            )
            assert response.status_code == 302
            assert PatientProfile.objects.filter(user="testuser").exists()