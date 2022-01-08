from datetime import timedelta
import factory
import pytest
from factory import Faker
from factory.django import DjangoModelFactory


from ..choices import BOOL_CHOICES
from ..models import ULTPlan
from ...users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class ULTPlanFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose_adjustment = Faker("pyint", min_value=20, max_value=150)
    goal_urate = factory.fuzzy.FuzzyFloat(5.0, 6.0)
    lab_interval = factory.LazyFunction(timedelta(days=42))
    titrating = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_titration = Faker('date')

    class Meta:
        model = ULTPlan
