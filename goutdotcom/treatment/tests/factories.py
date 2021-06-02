from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest

from goutdotcom.users.models import User

from goutdotcom.treatment.models import Allopurinol, Febuxostat, Colchicine, Probenecid, Ibuprofen, Naproxen, Meloxicam, Celecoxib, Methylprednisolone, Prednisone, Othertreat, Tinctureoftime, ALLOPURINOL_DOSE_CHOICES, ALLOPURINOL_SIDE_EFFECT_CHOICES, FEBUXOSTAT_DOSE_CHOICES, FEBUXOSTAT_SIDE_EFFECT_CHOICES, COLCHICINE_DOSE_CHOICES, COLCHICINE_SIDE_EFFECT_CHOICES, PROBENECID_DOSE_CHOICES, PROBENECID_SIDE_EFFECT_CHOICES, IBUPROFEN_DOSE_CHOICES, NSAID_SIDE_EFFECT_CHOICES, NAPROXEN_DOSE_CHOICES, MELOXICAM_DOSE_CHOICES, CELECOXIB_DOSE_CHOICES, PREDNISONE_SIDE_EFFECT_CHOICES, METHYLPREDNISOLONE_DOSE_CHOICES, INJECTION_SIDE_EFFECT_CHOICES, FREQ_CHOICES, BOOL_CHOICES
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class AllopurinolFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(ALLOPURINOL_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(ALLOPURINOL_SIDE_EFFECT_CHOICES)
    de_sensitized = factory.Iterator(BOOL_CHOICES, getter=lambda c:c[0])

    class Meta:
        model = Allopurinol

class FebuxostatFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(FEBUXOSTAT_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(FEBUXOSTAT_SIDE_EFFECT_CHOICES)

    class Meta:
        model = Febuxostat

class ColchicineFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(COLCHICINE_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(COLCHICINE_SIDE_EFFECT_CHOICES)
    as_prophylaxis = factory.Iterator(BOOL_CHOICES, getter=lambda c:c[0])

    class Meta:
        model = Colchicine

class IbuprofenFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(IBUPROFEN_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(NSAID_SIDE_EFFECT_CHOICES)
    as_prophylaxis = factory.Iterator(BOOL_CHOICES, getter=lambda c:c[0])
    
    class Meta:
        model = Ibuprofen

class NaproxenFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(NAPROXEN_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(NSAID_SIDE_EFFECT_CHOICES)
    as_prophylaxis = factory.Iterator(BOOL_CHOICES, getter=lambda c:c[0])
    
    class Meta:
        model = Naproxen

class MeloxicamFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(MELOXICAM_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(NSAID_SIDE_EFFECT_CHOICES)
    as_prophylaxis = factory.Iterator(BOOL_CHOICES, getter=lambda c:c[0])
    
    class Meta:
        model = Meloxicam

class CelecoxibFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(CELECOXIB_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(NSAID_SIDE_EFFECT_CHOICES)
    as_prophylaxis = factory.Iterator(BOOL_CHOICES, getter=lambda c:c[0])
    
    class Meta:
        model = Celecoxib

class PrednisoneFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = Faker("pyint", min_value=1, max_value=1000)
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(PREDNISONE_SIDE_EFFECT_CHOICES)
    as_prophylaxis = factory.Iterator(BOOL_CHOICES, getter=lambda c:c[0])
    
    class Meta:
        model = Prednisone

class MethylprednisoloneFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(METHYLPREDNISOLONE_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(INJECTION_SIDE_EFFECT_CHOICES)
    as_injection = factory.Iterator(BOOL_CHOICES, getter=lambda c:c[0])
    
    class Meta:
        model = Methylprednisolone

class ProbenecidFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dose = factory.Iterator(PROBENECID_DOSE_CHOICES, getter=lambda c:c[0])
    freq = factory.Iterator(FREQ_CHOICES)
    date_started = Faker('date')
    date_ended = Faker('date')
    side_effects = factory.Iterator(PROBENECID_SIDE_EFFECT_CHOICES)
    
    class Meta:
        model = Probenecid

class TinctureoftimeFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    duration = Faker("pyint", min_value=1, max_value=100)
    date_started = Faker('date')
    date_ended = Faker('date')
    
    class Meta:
        model = Tinctureoftime

class OthertreatFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = Faker("word")
    description = Faker('texts', nb_texts=1, max_nb_chars=250)
    date_started = Faker('date')
    date_ended = Faker('date')
    
    class Meta:
        model = Othertreat