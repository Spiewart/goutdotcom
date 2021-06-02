from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest
from goutdotcom.users.models import User

from goutdotcom.flare.models import Flare, JOINT_CHOICES, TREATMENT_CHOICES
from goutdotcom.lab.models import Urate, AST, ALT, Platelet, Hemoglobin, WBC, Creatinine
from goutdotcom.lab.tests.factories import UrateFactory
from goutdotcom.treatment.tests.factories import ColchicineFactory
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class FlareFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    location = factory.Iterator(JOINT_CHOICES)
    treatment = factory.Iterator(TREATMENT_CHOICES)

    if treatment == "Colcrys":
        colchicine = factory.SubFactory(ColchicineFactory)

    duration = Faker("pyint", min_value=1, max_value=100)
    urate = factory.SubFactory(UrateFactory)

    class Meta:
        model = Flare