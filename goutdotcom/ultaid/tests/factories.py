from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest

from goutdotcom.users.models import User

from ..models import ULTAid
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class ULTAidFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pyint", min_value=50, max_value=600)

    class Meta:
        model = ULTAid
