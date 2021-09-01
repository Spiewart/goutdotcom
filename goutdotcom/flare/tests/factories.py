from factory import Faker
from factory.django import DjangoModelFactory
import factory
import factory.fuzzy
import pytest

from goutdotcom.flare.choices import JOINT_CHOICES, TREATMENT_CHOICES, LAB_CHOICES
from goutdotcom.flare.models import Flare
from goutdotcom.lab.tests.factories import UrateFactory
from goutdotcom.treatment.tests.factories import ColchicineFactory
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class FlareFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    location = factory.fuzzy.FuzzyChoice(choices=JOINT_CHOICES, getter=lambda c: c[0])

    duration = Faker("pyint", min_value=1, max_value=100)
    labs = factory.fuzzy.FuzzyChoice(choices=LAB_CHOICES, getter=lambda c: c[0])

    urate = factory.SubFactory(UrateFactory, user=factory.SelfAttribute('..user'))

    class Meta:
        model = Flare

class FlareColcrysFactory(FlareFactory):
    treatment = "Colcrys"
    colchicine = factory.SubFactory(ColchicineFactory, user=factory.SelfAttribute('..user'))

factories = [FlareFactory, FlareColcrysFactory]
