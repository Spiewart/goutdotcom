import factory
import pytest
from django.db.models.signals import post_save
from factory import Faker
from factory.django import DjangoModelFactory

from goutdotcom.history.tests.factories import (
    AllopurinolHypersensitivityFactory,
    AnticoagulationFactory,
    BleedFactory,
    CHFFactory,
    CKDFactory,
    ColchicineInteractionsFactory,
    DiabetesFactory,
    ErosionsFactory,
    FebuxostatHypersensitivityFactory,
    HeartAttackFactory,
    HypertensionFactory,
    HyperuricemiaFactory,
    IBDFactory,
    OrganTransplantFactory,
    OsteoporosisFactory,
    StrokeFactory,
    TophiFactory,
    UrateKidneyStonesFactory,
    XOIInteractionsFactory,
)
from goutdotcom.profiles.models import MedicalProfile, PatientProfile, races, sexes
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.vitals.tests.factories import HeightFactory, WeightFactory

pytestmark = pytest.mark.django_db

GENDER_CHOICES = [x[0] for x in sexes]
RACE_CHOICES = [x[0] for x in races]


class PatientProfileFactory(DjangoModelFactory):
    class Meta:
        model = PatientProfile

    user = factory.SubFactory(UserFactory)
    date_of_birth = Faker("date_of_birth")
    drinks_per_week = Faker("pyint", min_value=1, max_value=110)
    gender = factory.Iterator(GENDER_CHOICES)
    race = factory.Iterator(RACE_CHOICES)
    height = factory.SubFactory(HeightFactory, user=factory.SelfAttribute("..user"))
    weight = factory.SubFactory(WeightFactory, user=factory.SelfAttribute("..user"))


@factory.django.mute_signals(post_save)
class MedicalProfileFactory(DjangoModelFactory):
    class Meta:
        model = MedicalProfile

    user = factory.SubFactory(UserFactory, medicalprofile=None)
    allopurinol_hypersensitivity = factory.SubFactory(
        AllopurinolHypersensitivityFactory, user=factory.SelfAttribute("..user")
    )
    CKD = factory.SubFactory(CKDFactory, user=factory.SelfAttribute("..user"))
    febuxostat_hypersensitivity = factory.SubFactory(
        FebuxostatHypersensitivityFactory, user=factory.SelfAttribute("..user")
    )
    hypertension = factory.SubFactory(HypertensionFactory, user=factory.SelfAttribute("..user"))
    hyperuricemia = factory.SubFactory(HyperuricemiaFactory, user=factory.SelfAttribute("..user"))
    IBD = factory.SubFactory(IBDFactory, user=factory.SelfAttribute("..user"))
    CHF = factory.SubFactory(CHFFactory, user=factory.SelfAttribute("..user"))
    diabetes = factory.SubFactory(DiabetesFactory, user=factory.SelfAttribute("..user"))
    erosions = factory.SubFactory(ErosionsFactory, user=factory.SelfAttribute("..user"))
    organ_transplant = factory.SubFactory(OrganTransplantFactory, user=factory.SelfAttribute("..user"))
    osteoporosis = factory.SubFactory(OsteoporosisFactory, user=factory.SelfAttribute("..user"))
    urate_kidney_stones = factory.SubFactory(UrateKidneyStonesFactory, user=factory.SelfAttribute("..user"))
    tophi = factory.SubFactory(TophiFactory, user=factory.SelfAttribute("..user"))
    anticoagulation = factory.SubFactory(AnticoagulationFactory, user=factory.SelfAttribute("..user"))
    bleed = factory.SubFactory(BleedFactory, user=factory.SelfAttribute("..user"))
    colchicine_interactions = factory.SubFactory(ColchicineInteractionsFactory, user=factory.SelfAttribute("..user"))
    heartattack = factory.SubFactory(HeartAttackFactory, user=factory.SelfAttribute("..user"))
    stroke = factory.SubFactory(StrokeFactory, user=factory.SelfAttribute("..user"))
    XOI_interactions = factory.SubFactory(XOIInteractionsFactory, user=factory.SelfAttribute("..user"))
