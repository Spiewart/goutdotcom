from decimal import *

import pytest

from .factories import FlareFactory

pytestmark = pytest.mark.django_db


class TestFlareMethods:
    def test_get_absolute_url(self):
        Flare = FlareFactory()
        assert Flare.get_absolute_url() == f"/flare/{Flare.pk}/"

    def test__str__(self):
        Flare = FlareFactory()
        assert Flare.__str__() == f"{(str(Flare.user), str(Flare.location))}"

    def test_flare_calculator(self):
        pass
