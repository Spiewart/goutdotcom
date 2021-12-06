import factory
import factory.fuzzy
import pytest
from django.db.models.fields import CharField
from factory import Faker
from factory.django import DjangoModelFactory

from goutdotcom.lab.tests.factories import UrateFactory
from goutdotcom.treatment.tests.factories import ColchicineFactory
from goutdotcom.users.tests.factories import UserFactory

from ...history.tests.factories import (
    CHFFactory,
    HeartAttackFactory,
    HypertensionFactory,
    PVDFactory,
    StrokeFactory,
)
from ..choices import (
    BOOL_CHOICES,
    CARDIAC_CHOICES,
    JOINT_CHOICES,
    LAB_CHOICES,
    TREATMENT_CHOICES,
)
from ..models import Flare

pytestmark = pytest.mark.django_db


class FlareFactory(DjangoModelFactory):
    monoarticular = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    male = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    prior_gout = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    onset = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    redness = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    firstmtp = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    location = factory.fuzzy.FuzzyChoice(JOINT_CHOICES, getter=lambda c: c[0])
    cardiacdisease = factory.fuzzy.FuzzyChoice(CARDIAC_CHOICES, getter=lambda c: c[0])
    hypertension = factory.SubFactory(HypertensionFactory)
    heartattack = factory.SubFactory(HeartAttackFactory)
    CHF = factory.SubFactory(CHFFactory)
    stroke = factory.SubFactory(StrokeFactory)
    PVD = factory.SubFactory(PVDFactory)
    duration = Faker("pyint", min_value=1, max_value=100)
    urate = factory.SubFactory(UrateFactory)
    treatment = factory.fuzzy.FuzzyChoice(choices=TREATMENT_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Flare
