import factory
import factory.fuzzy
import pytest
from factory.django import DjangoModelFactory

from ..choices import (
    BOOL_CHOICES,
    CHF_BOOL_CHOICES,
    LAST_MODIFIED_CHOICES,
    ORGAN_CHOICES,
)
from ..models import *

pytestmark = pytest.mark.django_db

# All factories utilizing choices need index 0 [0] to access value for each choice field, index 1 [1] is the label
class AlcoholFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    number = factory.Faker("pyint", min_value=0, max_value=100)
    wine = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    beer = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    liquor = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Alcohol


class AllopurinolHypersensitivityFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    rash = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    transaminitis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    cytopenia = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = AllopurinolHypersensitivity


class CKDFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    dialysis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    # Need to access CKD.Stage.choices for IntegerChoices (enum)
    stage = factory.fuzzy.FuzzyChoice(CKD.Stage.choices, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = CKD


class FebuxostatHypersensitivityFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    rash = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    transaminitis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    cytopenia = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = FebuxostatHypersensitivity

class FructoseFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Fructose

class HypertensionFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    medication = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Hypertension


class HyperuricemiaFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Hyperuricemia


class IBDFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = IBD


class GoutFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Gout


class CHFFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    systolic = factory.fuzzy.FuzzyChoice(CHF_BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = CHF


class DiabetesFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    type = factory.fuzzy.FuzzyChoice(Diabetes.Type.choices, getter=lambda c: c[0])
    insulin = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Diabetes


class ErosionsFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Erosions


class OrganTransplantFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    organ = factory.fuzzy.FuzzyChoice(ORGAN_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = OrganTransplant


class OsteoporosisFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Osteoporosis

class PVDFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = PVD

class ShellfishFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Shellfish

class UrateKidneyStonesFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = UrateKidneyStones


class TophiFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Tophi


class AnticoagulationFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Anticoagulation


class BleedFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Bleed


class ColchicineInteractionsFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = ColchicineInteractions


class HeartAttackFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = HeartAttack


class StrokeFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Stroke


class XOIInteractionsFactory(DjangoModelFactory):
    value = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])
    last_modified = factory.fuzzy.FuzzyChoice(LAST_MODIFIED_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = XOIInteractions
