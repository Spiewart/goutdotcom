from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest

from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.profiles.models import PatientProfile, sexes, races
from goutdotcom.vitals.models import Height, Weight
from goutdotcom.vitals.tests.factories import HeightFactory, WeightFactory

pytestmark = pytest.mark.django_db

GENDER_CHOICES = [x[0] for x in sexes]
RACE_CHOICES = [x[0] for x in races]

class PatientProfileFactory(DjangoModelFactory):
    class Meta:
        model = PatientProfile

    user = factory.SubFactory(UserFactory)
    date_of_birth = Faker("date_of_birth")
    drinks_per_week = Faker("pyint", min_value=1, max_value=110)
    gender = factory.Iterator(GENDER_CHOICES)
    race = factory.Iterator(RACE_CHOICES)
    height = factory.SubFactory(HeightFactory, user=factory.SelfAttribute('..user'))
    weight = factory.SubFactory(WeightFactory, user=factory.SelfAttribute('..user'))




