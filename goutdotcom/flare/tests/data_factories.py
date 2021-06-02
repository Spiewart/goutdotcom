from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest
from goutdotcom.users.models import User

from goutdotcom.flare.models import Flare
from goutdotcom.lab.models import Urate, AST, ALT, Platelet, Hemoglobin, WBC, Creatinine
from goutdotcom.lab.tests.data_factories import UrateSpiewFactory, JOINT_CHOICES
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class FlareUserFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    location = Faker(JOINT_CHOICES)
    treatment = 
    
    urate = factory.SubFactory(UrateSpiewFactory)

    class Meta:
        model = Flare