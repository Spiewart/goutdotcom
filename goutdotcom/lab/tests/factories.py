from factory import Faker
from factory.django import DjangoModelFactory
import factory

from goutdotcom.lab.models import Urate, AST, ALT, Platelet, Hemoglobin, WBC, Creatinine
from goutdotcom.users.models import User

class UrateFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    uric_acid = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Urate

class ALTFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    alt_sgpt = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = ALT


class ASTFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    ast_sgot = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = AST


class PlateletFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    platelets = Faker("pyint", min_value=1, max_value=1300)

    class Meta:
        model = Platelet


class WBCFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    white_blood_cells = Faker("pydecimal", left_digits=3, right_digits=1, positive=True, min_value=1, max_value=300)

    class Meta:
        model = WBC


class HemoglobinFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    hemoglobin = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=5, max_value=20)

    class Meta:
        model = Hemoglobin


class CreatinineFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    creatinine = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Creatinine
