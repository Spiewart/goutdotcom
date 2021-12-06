from decimal import *

import pytest

from .factories import FlareAidFactory

pytestmark = pytest.mark.django_db


class TestFlareAidMethods:
    def test_get_absolute_url(self):
        FlareAid = FlareAidFactory()
        assert FlareAid.get_absolute_url() == f"/flareaid/{FlareAid.pk}/"

    def test__str__(self):
        FlareAid = FlareAidFactory()
        assert FlareAid.__str__() == str(FlareAid.decision_aid())

    def test_monoarticular_aid(self):
        FlareAid = FlareAidFactory(monoarticular=True)
        assert (
            FlareAid.monoarticular_aid()
            == "Any monoarticular flare can be effectively treated with a corticosteroid injection by a rheumatologist or other provider."
        )

    def test_decision_aid_perfect_health(self):
        FlareAid = FlareAidFactory(perfect_health=True)
        assert FlareAid.decision_aid() == "NSAID"

    def test_decision_aid_perfect_health_isnone(self):
        FlareAid = FlareAidFactory(perfect_health=None)
        assert FlareAid.decision_aid() == "Need More Information"

    def test_decision_aid_CKD_no_diabetes(self):
        FlareAid = FlareAidFactory(perfect_health=False, ckd__value=True, diabetes__value=False)
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_CKD_and_diabetes(self):
        FlareAid = FlareAidFactory(perfect_health=False, ckd__value=True, diabetes__value=True)
        assert FlareAid.decision_aid() == "doctor"

    def test_decision_aid_bleed(self):
        FlareAid = FlareAidFactory(
            perfect_health=False,
            bleed__value=True,
            heartattack__value=False,
            stroke__value=False,
            anticoagulation__value=False,
            ibd__value=False,
            ckd__value=False,
            colchicine_interactions__value=False,
        )
        assert FlareAid.decision_aid() == "colchicine"

    def test_decision_aid_bleed_CKD_no_diabetes(self):
        FlareAid = FlareAidFactory(
            perfect_health=False,
            bleed__value=True,
            ckd__value=True,
            diabetes__value=False,
            colchicine_interactions__value=False,
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_bleed_colchicine_interactions(self):
        FlareAid = FlareAidFactory(
            perfect_health=False, bleed__value=True, ckd__value=False, colchicine_interactions__value=True
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_bleed_colchicine_interactions(self):
        FlareAid = FlareAidFactory(
            perfect_health=False, bleed__value=True, ckd__value=False, colchicine_interactions__value=True
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_heartattack_CKD_no_diabetes(self):
        FlareAid = FlareAidFactory(
            perfect_health=False,
            heartattack__value=True,
            ckd__value=True,
            diabetes__value=False,
            colchicine_interactions__value=False,
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_heartattack_colchicine_interactions(self):
        FlareAid = FlareAidFactory(
            perfect_health=False, heartattack__value=True, ckd__value=False, colchicine_interactions__value=True
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_stroke_CKD_no_diabetes(self):
        FlareAid = FlareAidFactory(
            perfect_health=False,
            stroke__value=True,
            ckd__value=True,
            diabetes__value=False,
            colchicine_interactions__value=False,
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_stroke_colchicine_interactions(self):
        FlareAid = FlareAidFactory(
            perfect_health=False, stroke__value=True, ckd__value=False, colchicine_interactions__value=True
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_anticoagulation_CKD_no_diabetes(self):
        FlareAid = FlareAidFactory(
            perfect_health=False,
            anticoagulation__value=True,
            ckd__value=True,
            diabetes__value=False,
            colchicine_interactions__value=False,
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_anticoagulation_colchicine_interactions(self):
        FlareAid = FlareAidFactory(
            perfect_health=False, anticoagulation__value=True, ckd__value=False, colchicine_interactions__value=True
        )
        assert FlareAid.decision_aid() == "steroids"
        # NEED TO CHANGE MODEL TO MAKE IBD WORK, IT IS COMMENTED OUT FOR SOME REASON NOT WORKING


"""
    def test_decision_aid_ibd_CKD_no_diabetes(self):
        FlareAid = FlareAidFactory(
            perfect_health=False, ibd__value=True, ckd__value=True, colchicine_interactions__value=False, diabetes__value=False
        )
        assert FlareAid.decision_aid() == "steroids"

    def test_decision_aid_ibd_colchicine_interactions(self):
        FlareAid = FlareAidFactory(
            perfect_health=False, ibd__value=True, ckd__value=False, colchicine_interactions__value=True
        )
        assert FlareAid.decision_aid() == "steroids"
"""
