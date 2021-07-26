from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.users.models import User
import pytest

from decimal import *

from .factories import WeightFactory

pytestmark = pytest.mark.django_db

class TestWeightMethods:
    def test__str__(self):
        weight = WeightFactory()
        assert(weight.__str__() == str(weight.value))

    def test__unicode__(self):
        weight = WeightFactory()
        assert(weight.__unicode__() == str(weight.name))

    def test_get_absolute_url(self):
        weight = WeightFactory()
        assert weight.get_absolute_url() == f"/vitals/weight/{weight.pk}/"

    def test_convert_pounds_to_kg(self):
        weight = WeightFactory(value=100)
        assert round(weight.value / 2.205, 1) == 45.4
