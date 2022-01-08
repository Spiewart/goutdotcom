import factory
import pytest
from factory import Faker
from factory.django import DjangoModelFactory

from goutdotcom.lab.models import (
    ALT,
    AST,
    WBC,
    Creatinine,
    Hemoglobin,
    LabCheck,
    Platelet,
    Urate,
)
from goutdotcom.ultplan.tests.factories import ULTPlanFactory
from goutdotcom.users.tests.factories import UserFactory

from ..choices import BOOL_CHOICES

pytestmark = pytest.mark.django_db


class UrateFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    value = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Urate


class ALTFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    value = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = ALT


class ASTFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    value = Faker("pyint", min_value=1, max_value=9999)

    class Meta:
        model = AST


class PlateletFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    value = Faker("pyint", min_value=1, max_value=1300)

    class Meta:
        model = Platelet


class WBCFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    value = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=99)

    class Meta:
        model = WBC


class HemoglobinFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    value = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=5, max_value=20)

    class Meta:
        model = Hemoglobin


class CreatinineFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    value = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Creatinine


class LabCheckFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    alt = factory.SubFactory(
        ALTFactory, user=factory.SelfAttribute("..user"), ultplan=factory.SelfAttribute("..ultplan")
    )
    ast = factory.SubFactory(
        ASTFactory, user=factory.SelfAttribute("..user"), ultplan=factory.SelfAttribute("..ultplan")
    )
    creatinine = factory.SubFactory(
        CreatinineFactory, user=factory.SelfAttribute("..user"), ultplan=factory.SelfAttribute("..ultplan")
    )
    hemoglobin = factory.SubFactory(
        HemoglobinFactory, user=factory.SelfAttribute("..user"), ultplan=factory.SelfAttribute("..ultplan")
    )
    platelet = factory.SubFactory(
        PlateletFactory, user=factory.SelfAttribute("..user"), ultplan=factory.SelfAttribute("..ultplan")
    )
    wbc = factory.SubFactory(
        WBCFactory, user=factory.SelfAttribute("..user"), ultplan=factory.SelfAttribute("..ultplan")
    )
    urate = factory.SubFactory(
        UrateFactory, user=factory.SelfAttribute("..user"), ultplan=factory.SelfAttribute("..ultplan")
    )
    due = factory.Faker("date")
    completed = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    completed_date = factory.Faker("date")

    class Meta:
        model = LabCheck
