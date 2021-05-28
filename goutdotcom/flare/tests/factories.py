from factory import Faker
from factory.django import DjangoModelFactory
import factory
import pytest
from goutdotcom.users.models import User

from goutdotcom.flare.models import Flare
from goutdotcom.lab.models import Urate, AST, ALT, Platelet, Hemoglobin, WBC, Creatinine
from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

class FlareFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    location = 
    treatment = 
    
    urate = Faker("pydecimal", left_digits=2, right_digits=1, positive=True, min_value=1, max_value=30)

    class Meta:
        model = Flare