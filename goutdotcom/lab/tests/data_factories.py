from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest
from goutdotcom.users.models import User

from goutdotcom.lab.models import Urate, AST, ALT, Platelet, Hemoglobin, WBC, Creatinine
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class UrateSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    uric_acid = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Urate

class UrateUserFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    uric_acid = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Urate

class ALTSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    alt_sgpt = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = ALT

class ALTUserFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    alt_sgpt = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = ALT

class ASTSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    ast_sgot = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = AST

class ASTUserFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    ast_sgot = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = AST

class PlateletSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    platelets = Faker("pyint", min_value=1, max_value=1300)

    class Meta:
        model = Platelet

class PlateletUserFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    platelets = Faker("pyint", min_value=1, max_value=1300)

    class Meta:
        model = Platelet

class WBCSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    white_blood_cells = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=99)

    class Meta:
        model = WBC

class WBCUserFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    white_blood_cells = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=99)

    class Meta:
        model = WBC

class HemoglobinSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    hemoglobin = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=5, max_value=20)

    class Meta:
        model = Hemoglobin

class HemoglobinUserFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    hemoglobin = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=5, max_value=20)

    class Meta:
        model = Hemoglobin

class CreatinineSpiewFactory(DjangoModelFactory):
    user = User.objects.get(username="spiew")
    creatinine = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Creatinine

class CreatinineUserFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    creatinine = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Creatinine