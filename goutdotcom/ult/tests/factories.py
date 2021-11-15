import factory
import pytest
from factory import Faker
from factory.django import DjangoModelFactory

from goutdotcom.users.models import User

from ...history.models import *
from ...history.tests.factories import (
    CKDFactory,
    ErosionsFactory,
    HyperuricemiaFactory,
    TophiFactory,
    UrateKidneyStonesFactory,
)
from ...profiles.models import MedicalProfile
from ...profiles.tests.factories import MedicalProfileFactory
from ...users.models import User
from ...users.tests.factories import UserFactory
from ..choices import FREQ_CHOICES, ULT_CHOICES
from ..models import ULT


class ULTFactory(DjangoModelFactory):
    num_flares = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    freq_flares = factory.fuzzy.FuzzyChoice(ULT_CHOICES, getter=lambda c: c[0])
    erosions = factory.SubFactory(ErosionsFactory)
    tophi = factory.SubFactory(TophiFactory)
    stones = factory.SubFactory(UrateKidneyStonesFactory)
    ckd = factory.SubFactory(CKDFactory)
    hyperuricemia = factory.SubFactory(HyperuricemiaFactory)

    class Meta:
        model = ULT
