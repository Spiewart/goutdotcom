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
from ..models import ULTAid

pytestmark = pytest.mark.django_db

class ULTAidFactory(DjangoModelFactory):
    ckd = factory.SubFactory(CKDFactory)
    XOI_interactions = factory.SubFactory(XOIInteractionsFactory)
    organ_transplant = factory.SubFactory(OrganTransplantFactory)
    allopurinol_hypersensitivity = factory.SubFactory(AllopurinolHypersensitivityFactory)
    febuxostat_hypersensitivity = factory.SubFactory(FebuxostatHypersensitivityFactory)
    heartattack = factory.SubFactory(HeartAttackFactory)
    stroke = factory.SubFactory(StrokeFactory)

    class Meta:
        model = ULTAid
