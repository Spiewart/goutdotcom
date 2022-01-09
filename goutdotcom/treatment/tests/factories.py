from factory import Faker
from factory.django import DjangoModelFactory
import factory
import factory.fuzzy
import pytest

from ...treatment.choices import ALLOPURINOL_DOSE_CHOICES, ALLOPURINOL_SIDE_EFFECT_CHOICES, FEBUXOSTAT_DOSE_CHOICES, FEBUXOSTAT_SIDE_EFFECT_CHOICES, COLCHICINE_DOSE_CHOICES, COLCHICINE_SIDE_EFFECT_CHOICES, PROBENECID_DOSE_CHOICES, PROBENECID_SIDE_EFFECT_CHOICES, IBUPROFEN_DOSE_CHOICES, NSAID_SIDE_EFFECT_CHOICES, NAPROXEN_DOSE_CHOICES, MELOXICAM_DOSE_CHOICES, CELECOXIB_DOSE_CHOICES, PREDNISONE_SIDE_EFFECT_CHOICES, METHYLPREDNISOLONE_DOSE_CHOICES, INJECTION_SIDE_EFFECT_CHOICES, FREQ_CHOICES, BOOL_CHOICES
from ...treatment.models import Allopurinol, Febuxostat, Colchicine, Probenecid, Ibuprofen, Naproxen, Meloxicam, Celecoxib, Methylprednisolone, Prednisone, Othertreat, Tinctureoftime
from ...ultplan.tests.factories import ULTPlanFactory
from ...users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class TreatmentFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    date_started = Faker('date')
    date_ended = Faker('date')

    class Meta:
        abstract = True


class AllopurinolFactory(TreatmentFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    dose = factory.fuzzy.FuzzyChoice(ALLOPURINOL_DOSE_CHOICES, getter=lambda c: c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(ALLOPURINOL_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])
    de_sensitized = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Allopurinol


class FebuxostatFactory(TreatmentFactory):
    user = factory.SubFactory(UserFactory)
    ultplan = factory.SubFactory(ULTPlanFactory, user=factory.SelfAttribute("..user"))
    dose = factory.fuzzy.FuzzyChoice(FEBUXOSTAT_DOSE_CHOICES, getter=lambda c: c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(FEBUXOSTAT_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Febuxostat


class ColchicineFactory(TreatmentFactory):
    dose = factory.fuzzy.FuzzyChoice(COLCHICINE_DOSE_CHOICES, getter=lambda c: c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(COLCHICINE_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])
    as_prophylaxis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Colchicine


class IbuprofenFactory(TreatmentFactory):
    dose = factory.fuzzy.FuzzyChoice(IBUPROFEN_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(NSAID_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])
    as_prophylaxis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Ibuprofen


class NaproxenFactory(TreatmentFactory):
    dose = factory.fuzzy.FuzzyChoice(NAPROXEN_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(NSAID_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])
    as_prophylaxis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Naproxen


class MeloxicamFactory(TreatmentFactory):
    dose = factory.fuzzy.FuzzyChoice(MELOXICAM_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(NSAID_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])
    as_prophylaxis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Meloxicam


class CelecoxibFactory(TreatmentFactory):
    dose = factory.fuzzy.FuzzyChoice(CELECOXIB_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(NSAID_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])
    as_prophylaxis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Celecoxib


class PrednisoneFactory(TreatmentFactory):
    dose = Faker("pyint", min_value=1, max_value=1000)
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(PREDNISONE_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])
    as_prophylaxis = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Prednisone


class MethylprednisoloneFactory(TreatmentFactory):
    dose = factory.fuzzy.FuzzyChoice(METHYLPREDNISOLONE_DOSE_CHOICES, getter=lambda c: c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(INJECTION_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])
    as_injection = factory.fuzzy.FuzzyChoice(BOOL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Methylprednisolone


class ProbenecidFactory(TreatmentFactory):
    dose = factory.fuzzy.FuzzyChoice(PROBENECID_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.fuzzy.FuzzyChoice(FREQ_CHOICES, getter=lambda c: c[0])
    side_effects = factory.fuzzy.FuzzyChoice(PROBENECID_SIDE_EFFECT_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Probenecid


class TinctureoftimeFactory(TreatmentFactory):
    duration = Faker("pyint", min_value=1, max_value=100)

    class Meta:
        model = Tinctureoftime


class OthertreatFactory(TreatmentFactory):
    name = Faker("word")
    description = Faker('texts', nb_texts=1, max_nb_chars=250)

    class Meta:
        model = Othertreat
