from django.apps import apps
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from goutdotcom.profiles.tests.factories import PatientProfileFactory
from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.vitals.tests.factories import HeightFactory, WeightFactory

from ..forms import PatientProfileForm
from ..models import PatientProfile
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
        request = self.factory.post(PatientProfileCreate, data=self.profile_data)
        request.user = self.user
        response = PatientProfileCreate.as_view()(request)
        self.assertRedirects(response, request.user.get_absolute_url(), fetch_redirect_response=False)

    def test_get_context_data(self):
        request = self.factory.get('/profiles/create')
        request.user = self.user
        response = PatientProfileCreate.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn('height_form', response.context_data)
        self.assertIn('weight_form', response.context_data)

    def test_get_object(self):
        request = self.factory.get('/profiles/create')
        request.user = self.user
        view = PatientProfileCreate()
        self.assertAlmostEquals(view.model, PatientProfile)

    def test_post(self):
        pass


class TestUpdateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.profile = PatientProfileFactory(user=self.user)
        self.kwargs = {'user':self.user, 'pk':self.profile.pk}
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
        self.update_url = reverse('profiles:update', kwargs={'user':self.user, 'pk':self.profile.pk})

    def test_get_sucess_url(self):
        request = self.factory.post(self.update_url, data=self.profile_data)
        request.user = self.user
        response = PatientProfileUpdate.as_view()(request, **self.kwargs)
        self.assertRedirects(response, request.user.get_absolute_url(), fetch_redirect_response=False)

    def test_get_context_data(self):
        request = self.factory.get(self.update_url)
        request.user = self.user
        response = PatientProfileUpdate.as_view()(request, pk=self.profile.pk)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn('height_form', response.context_data)
        self.assertIn('weight_form', response.context_data)
