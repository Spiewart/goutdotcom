from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest

from goutdotcom.users.models import User

from goutdotcom.vitals.models import Weight, Height
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class WeightFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pyint", min_value=50, max_value=600)

    class Meta:
        model = Weight


class HeightFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pyint", min_value=40, max_value=120)

    class Meta:
        model = Height

