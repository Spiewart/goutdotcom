from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.profiles.models import PatientProfile

class PatientProfileFactory(DjangoModelFactory):

    user = UserFactory()
    date_of_birth = 
    age = 
    drinks_per_week =

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]