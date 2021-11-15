import pytest

from .factories import ULTFactory

pytestmark = pytest.mark.django_db


class TestULTMethods:
    def test__str__(self):
        ULT = ULTFactory()
        assert ULT.__str__() == str(ULT.calculator())

    def test_get_absolute_url(self):
        ULT = ULTFactory()
        assert ULT.get_absolute_url() == f"/ult/{ULT.pk}/"

    def test_calculator(self):
        ULT = ULTFactory(num_flares="Zero")
        assert ULT.calculator() == "Not Indicated"
