from django.test import TestCase
from django.contrib.auth.models import User, Group
from gout.models import Urate, Creatinine, Patient

from factory.django import DjangoModelFactory
#import factory

class UserFactory(DjangoModelFactory):

    username = factory.Sequence('testuser{}'.format)
    email = factory.Sequence('testuser{}@company.com'.format)

    class Meta:
        model = User

class UrateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_owner = UserFactory()
        test_owner.save()
        test_patient = Patient(first_name="Dave", last_name="Ewart", age=35, gender="male", mrn=10001111, email="test_gmail@gmail.com", owner=test_owner)
        test_patient.save()
        Urate.objects.create(uric_acid=4.7, date=11/11/2020, patient=test_patient)

    def test_first_name_label(self):
        urate = Urate.objects.get(id=1)
        field_label = uric_acid._meta.get_field('uric_acid').verbose_name
        self.assertEquals(field_label, 'uric_acid')
