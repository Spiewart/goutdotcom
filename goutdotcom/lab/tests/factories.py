from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest

from goutdotcom.lab.models import Urate, AST, ALT, Platelet, Hemoglobin, WBC, Creatinine
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class UrateFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    uric_acid = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Urate

class UrateSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    uric_acid = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Urate

class ALTFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    alt_sgpt = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = ALT


class ALTSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    alt_sgpt = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = ALT

class ASTFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ast_sgot = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = AST


class ASTSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    ast_sgot = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = AST

class PlateletFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    platelets = Faker("pyint", min_value=1, max_value=1300)

    class Meta:
        model = Platelet


class PlateletSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    platelets = Faker("pyint", min_value=1, max_value=1300)

    class Meta:
        model = Platelet

class WBCFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    white_blood_cells = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=300)

    class Meta:
        model = WBC


class WBCSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    white_blood_cells = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=300)

    class Meta:
        model = WBC

class HemoglobinFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    hemoglobin = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=5, max_value=20)

    class Meta:
        model = Hemoglobin


class HemoglobinSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    hemoglobin = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=5, max_value=20)

    class Meta:
        model = Hemoglobin

class CreatinineFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    creatinine = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Creatinine


class CreatinineSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    creatinine = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Creatinine
