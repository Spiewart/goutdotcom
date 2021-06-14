from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest

from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.profiles.models import PatientProfile

pytestmark = pytest.mark.django_db

class PatientProfileFactory(DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    date_of_birth = Faker("date", pattern='%Y-%m-%d', end_datetime=None)
    drinks_per_week = Faker("pyint", min_value=1, max_value=110)

    class Meta:
        model = PatientProfile