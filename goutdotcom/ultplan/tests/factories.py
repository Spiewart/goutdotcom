import datetime

import factory
import pytest
from factory import fuzzy
from factory.django import DjangoModelFactory

from ...users.tests.factories import UserFactory
from ..choices import BOOL_CHOICES
from ..models import ULTPlan

pytestmark = pytest.mark.django_db


class ULTPlanFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose_adjustment = factory.Faker("pyint", min_value=20, max_value=150)
    goal_urate = factory.fuzzy.FuzzyFloat(5.0, 6.0)
    lab_interval = datetime.timedelta(days=42)
    titrating = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_titration = factory.Faker("date")

    class Meta:
        model = ULTPlan
