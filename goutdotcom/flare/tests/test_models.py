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

    def test_flare_calculator_monoarticular(self):
        Flare = FlareFactory(
            monoarticular=True,
        )
        assert (
            Flare.flare_calculator().get("caveat")
            == "This calculator has only been validated for monoarticular (1 joint) flares. It can't necessarily be applied to polyarticular (more than 1 joint) flares."
        )
