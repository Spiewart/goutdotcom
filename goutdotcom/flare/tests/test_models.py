from decimal import *

import pytest

from ...history.tests.factories import (
    AnginaFactory,
    CHFFactory,
    HeartAttackFactory,
    HypertensionFactory,
    PVDFactory,
    StrokeFactory,
)
from ...lab.tests.factories import UrateFactory
from ..choices import *
from ..models import Flare
from .factories import FlareFactory

pytestmark = pytest.mark.django_db


class TestFlareMethods:
    def test_get_absolute_url(self):
        flare = FlareFactory()
        assert flare.get_absolute_url() == f"/flare/{flare.pk}/"

    def test__str__(self):
        flare = FlareFactory()
        assert flare.__str__() == f"{(str(flare.user), str(flare.location))}"

    # locations() method tests
    def test_locations_monoarticular_podagra(self):
        flare = FlareFactory(monoarticular=True, firstmtp=True, location=[""])
        assert flare.locations() == "monoarticular, big toe"

    def test_locations_monoarticular_not_podagra_one_location(self):
        flare = FlareFactory(monoarticular=True, firstmtp=False, location=["Right hip"])
        assert flare.locations() == "monoarticular, right hip"

    def test_locations_monoarticular_not_podagra_multiple_locations(self):
        flare = FlareFactory(monoarticular=True, firstmtp=False, location=["Right hip", "Left hand"])
        assert flare.locations() == "monoarticular, right hip, left hand"

    def test_locations_polyarticular_podagra_no_location(self):
        flare = FlareFactory(monoarticular=False, firstmtp=True, location=[])
        assert flare.locations() == "polyarticular, big toe"

    def test_locations_polyarticular_podagra_one_location(self):
        flare = FlareFactory(monoarticular=False, firstmtp=True, location=["Right hip"])
        assert flare.locations() == "polyarticular, big toe, right hip"

    def test_locations_polyarticular_podagra_many_location(self):
        flare = FlareFactory(monoarticular=False, firstmtp=True, location=["Right hip", "Right hand"])
        assert flare.locations() == "polyarticular, big toe, right hip, right hand"

    def test_locations_polyarticular_not_podagra_one_location(self):
        flare = FlareFactory(monoarticular=False, firstmtp=False, location=["Right knee"])
        assert flare.locations() == "polyarticular, right knee"

    def test_locations_polyarticular_not_podagra_many_location(self):
        flare = FlareFactory(monoarticular=False, firstmtp=False, location=["Left hip", "Right ankle"])
        assert flare.locations() == "polyarticular, left hip, right ankle"

    def test_locations_polyarticular_not_podagra_no_location(self):
        flare = FlareFactory(monoarticular=False, firstmtp=False, location=[])
        assert flare.locations() == "polyarticular"

    # flare_calculator() method tests
    def test_flare_calculator_not_monoarticular(self):
        flare = FlareFactory(
            monoarticular=False,
            male=False,
            prior_gout=False,
            onset=False,
            redness=False,
            firstmtp=False,
            location=[],
            angina=AnginaFactory(value=False),
            hypertension=HypertensionFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            CHF=CHFFactory(value=False),
            stroke=StrokeFactory(value=False),
            PVD=PVDFactory(value=False),
        )
        assert (
            flare.flare_calculator().get("caveat")
            == "This calculator has only been validated for monoarticular (1 joint) flares. It can't necessarily be applied to polyarticular (more than 1 joint) flares."
        )

    def test_flare_calculator_male(self):
        flare = FlareFactory(
            monoarticular=False,
            male=True,
            prior_gout=False,
            onset=False,
            redness=False,
            firstmtp=False,
            location=[],
            angina=AnginaFactory(value=False),
            hypertension=HypertensionFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            CHF=CHFFactory(value=False),
            stroke=StrokeFactory(value=False),
            PVD=PVDFactory(value=False),
            urate=UrateFactory(value=5.9),
        )
        assert flare.flare_calculator().get("result") == UNLIKELY
        assert flare.flare_calculator().get("likelihood") == LOWRANGE
        assert flare.flare_calculator().get("prevalence") == LOWPREV

    def test_flare_calculator_male_prior_gout(self):
        flare = FlareFactory(
            monoarticular=False,
            male=True,
            prior_gout=True,
            onset=False,
            redness=False,
            firstmtp=False,
            location=[],
            angina=AnginaFactory(value=False),
            hypertension=HypertensionFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            CHF=CHFFactory(value=False),
            stroke=StrokeFactory(value=False),
            PVD=PVDFactory(value=False),
            urate=UrateFactory(value=5.9),
        )
        assert flare.flare_calculator().get("result") == EQUIVOCAL
        assert flare.flare_calculator().get("likelihood") == MIDRANGE
        assert flare.flare_calculator().get("prevalence") == MODPREV

    def test_flare_calculator_male_prior_gout_hypertension_urate(self):
        flare = FlareFactory(
            monoarticular=False,
            male=True,
            prior_gout=True,
            onset=False,
            redness=False,
            firstmtp=False,
            location=[],
            angina=AnginaFactory(value=False),
            hypertension=HypertensionFactory(value=True),
            heartattack=HeartAttackFactory(value=False),
            CHF=CHFFactory(value=False),
            stroke=StrokeFactory(value=False),
            PVD=PVDFactory(value=False),
            urate=UrateFactory(value=6.9),
        )
        assert flare.flare_calculator().get("result") == LIKELY
        assert flare.flare_calculator().get("likelihood") == HIGHRANGE
        assert flare.flare_calculator().get("prevalence") == HIGHPREV

    def test_flare_calculator_male_prior_gout_multiple_cardiac_risks(self):
        flare = FlareFactory(
            monoarticular=False,
            male=True,
            prior_gout=True,
            onset=False,
            redness=False,
            firstmtp=False,
            location=[],
            angina=AnginaFactory(value=False),
            hypertension=HypertensionFactory(value=True),
            heartattack=HeartAttackFactory(value=True),
            CHF=CHFFactory(value=True),
            stroke=StrokeFactory(value=True),
            PVD=PVDFactory(value=True),
            urate=UrateFactory(value=4.9),
        )
        assert flare.flare_calculator().get("result") == EQUIVOCAL
        assert flare.flare_calculator().get("likelihood") == MIDRANGE
        assert flare.flare_calculator().get("prevalence") == MODPREV
