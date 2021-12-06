import factory
import pytest
from factory import Faker
from factory.django import DjangoModelFactory

from goutdotcom.lab.models import ALT, AST, WBC, Creatinine, Hemoglobin, Platelet, Urate
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class UrateFactory(DjangoModelFactory):
    value = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Urate


class ALTFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = ALT


class ASTFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = AST


class PlateletFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pyint", min_value=1, max_value=1300)

    class Meta:
        model = Platelet


class WBCFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=99)

    class Meta:
        model = WBC


class HemoglobinFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=5, max_value=20)

    class Meta:
        model = Hemoglobin


class CreatinineFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Creatinine
