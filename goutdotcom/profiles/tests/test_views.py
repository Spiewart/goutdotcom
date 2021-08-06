from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.vitals.tests.factories import HeightFactory, WeightFactory
from django.apps import apps
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from goutdotcom.profiles.tests.factories import PatientProfileFactory
from goutdotcom.vitals.tests.factories import HeightFactory, WeightFactory
from ..forms import PatientProfileForm
from ..views import PatientProfileCreate, PatientProfileUpdate

class TestCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.create_url = reverse('profiles:create')
        self.height = HeightFactory(user=self.user)
        self.weight = WeightFactory(user=self.user)
        self.profile_data = {
            'user': self.user,
            'bio': 'Humphrey Bogart\'s profile',
            'date_of_birth': '12/25/1899',
            'gender': 'male',
            'race': 'white',
            'height': self.height,
            'weight': self.weight,
            'drinks_per_week': 60,
        }

    def test_form_valid(self):
        form = PatientProfileForm(data=self.profile_data)
        self.assertTrue(form.is_valid())

    def test_get_sucess_url(self):
        request = self.factory.get(self.create_url)
        request.user = self.user
        response = PatientProfileCreate.as_view()(request, self.profile_data, user=self.user)
        self.assertRedirects(response, request.user.get_absolute_url())
