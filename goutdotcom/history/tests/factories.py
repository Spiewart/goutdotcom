import factory
import factory.fuzzy
import pytest
from factory import Faker
from factory.django import DjangoModelFactory

from goutdotcom.users.models import User

from ...users.models import User
from ...users.tests.factories import UserFactory
from ..choices import BOOL_CHOICES, LAST_MODIFIED_CHOICES
from ..models import *

pytestmark = pytest.mark.django_db


class CKDFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    dialysis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    stage = factory.fuzzy.FuzzyChoice(choices=CKD.stage.choices.choices)
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = CKD
