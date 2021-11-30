import factory
import pytest
from factory.django import DjangoModelFactory

from ...history.tests.factories import (
    AnticoagulationFactory,
    BleedFactory,
    CKDFactory,
    ColchicineInteractionsFactory,
    DiabetesFactory,
    HeartAttackFactory,
    IBDFactory,
    OsteoporosisFactory,
    StrokeFactory,
)
from ..choices import BOOL_CHOICES
from ..models import FlareAid

pytestmark = pytest.mark.django_db


class FlareAidFactory(DjangoModelFactory):
    perfect_health = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    monoarticular = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    anticoagulation = factory.SubFactory(AnticoagulationFactory)
    bleed = factory.SubFactory(BleedFactory)
    ckd = factory.SubFactory(CKDFactory)
    colchicine_interactions = factory.SubFactory(ColchicineInteractionsFactory)
    diabetes = factory.SubFactory(DiabetesFactory)
    heartattack = factory.SubFactory(HeartAttackFactory)
    ibd = factory.SubFactory(IBDFactory)
    osteoporosis = factory.SubFactory(OsteoporosisFactory)
    stroke = factory.SubFactory(StrokeFactory)

    class Meta:
        model = FlareAid
