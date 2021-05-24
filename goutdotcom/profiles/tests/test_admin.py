import pytest
from django.urls import reverse

from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.profiles.models import PatientProfile
from goutdotcom.profiles.tests.factories import PatientProfileFactory

pytestmark = pytest.mark.django_db

class TestPatientProfileAdmin:
        def test_add(self, admin_client):
            url = reverse("admin:profiles_patientprofile_add")
            response = admin_client.get(url)
            profile = PatientProfileFactory()
            assert response.status_code == 200

            response = admin_client.post(
                url,
                data={
                    "user": profile.user,
                },
            )
            #assert response.status_code == 302
            assert PatientProfile.objects.get(user=profile.user).exists()