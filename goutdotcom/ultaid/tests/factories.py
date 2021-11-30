import factory
import pytest
from factory import Faker
from factory.django import DjangoModelFactory

from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

from ...history.tests.factories import (
    AllopurinolHypersensitivityFactory,
    CKDFactory,
    FebuxostatHypersensitivityFactory,
    HeartAttackFactory,
    OrganTransplantFactory,
    StrokeFactory,
    XOIInteractionsFactory,
)
from ..choices import BOOL_CHOICES
from ..models import ULTAid

pytestmark = pytest.mark.django_db


class ULTAidFactory(DjangoModelFactory):
    need = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    want = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    ckd = factory.SubFactory(CKDFactory)
    XOI_interactions = factory.SubFactory(XOIInteractionsFactory)
    organ_transplant = factory.SubFactory(OrganTransplantFactory)
    allopurinol_hypersensitivity = factory.SubFactory(AllopurinolHypersensitivityFactory)
    febuxostat_hypersensitivity = factory.SubFactory(FebuxostatHypersensitivityFactory)
    heartattack = factory.SubFactory(HeartAttackFactory)
    stroke = factory.SubFactory(StrokeFactory)

    class Meta:
        model = ULTAid
