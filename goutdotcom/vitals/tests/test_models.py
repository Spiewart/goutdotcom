from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.users.models import User
import pytest

from decimal import *
from math import floor

from .factories import WeightFactory, HeightFactory

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

class TestHeightMethods:
    def test__str__(self):
        weight = WeightFactory()
        assert(weight.__str__() == str(weight.value))

    def test__unicode__(self):
        weight = WeightFactory()
        assert(weight.__unicode__() == str(weight.name))

    def test_get_absolute_url(self):
        weight = WeightFactory()
        assert weight.get_absolute_url() == f"/vitals/weight/{weight.pk}/"

    def test_convert_inches_to_feet(self):
        height = HeightFactory(value=75)
        height_feet = floor(height.value / 12)
        height_inches = height.value - height_feet * 12
        assert height_feet == 6
        assert height_inches == 3
        assert height.convert_inches_to_feet() == "6 foot 3 inches"

    def test_convert_inches_to_meters(self):
        height = HeightFactory(value=75)
        assert round(height.value / 39.37, 2) == 1.91

