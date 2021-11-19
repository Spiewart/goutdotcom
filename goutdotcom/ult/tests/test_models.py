import pytest

from goutdotcom.history.tests.factories import (
    HyperuricemiaFactory,
    TophiFactory,
    UrateKidneyStonesFactory,
)

from ...history.tests.factories import (
    CKDFactory,
    ErosionsFactory,
    HyperuricemiaFactory,
    TophiFactory,
    UrateKidneyStonesFactory,
)
from .factories import ULTFactory

pytestmark = pytest.mark.django_db


class TestULTMethods:
    def test__str__(self):
        ULT = ULTFactory()
        assert ULT.__str__() == str(ULT.calculator())

    def test_get_absolute_url(self):
        ULT = ULTFactory()
        assert ULT.get_absolute_url() == f"/ult/{ULT.pk}/"

    def test_calculator_zeroflares(self):
        ULT = ULTFactory(
            num_flares="zero",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Not Indicated"

    def test_calculator_oneflare_noindication(self):
        ULT = ULTFactory(
            num_flares="one",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Not Indicated"

    def test_calculator_oneflare_indication_ckd(self):
        ULT = ULTFactory(
            num_flares="one",
            ckd=CKDFactory(value=True, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Conditional"

    def test_calculator_oneflare_indication_erosions(self):
        ULT = ULTFactory(
            num_flares="one",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=True),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Indicated"

    def test_calculator_oneflare_indication_stones(self):
        ULT = ULTFactory(
            num_flares="one",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=True),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Conditional"

    def test_calculator_oneflare_indication_uric_acid(self):
        ULT = ULTFactory(
            num_flares="one",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=True),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Conditional"

    def test_calculator_oneflare_indication_tophi(self):
        ULT = ULTFactory(
            num_flares="one",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=True),
        )
        assert ULT.calculator() == "Indicated"

    def test_calculator_dialysis(self):
        ULT = ULTFactory(
            num_flares="one",
            ckd=CKDFactory(value=True, dialysis=True),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Dialysis"

    def test_calculator_zeroflares_erosions(self):
        ULT = ULTFactory(
            num_flares="zero",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=True),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Indicated"

    def test_calculator_zeroflares_tophi(self):
        ULT = ULTFactory(
            num_flares="zero",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=True),
        )
        assert ULT.calculator() == "Indicated"

    def test_calculator_twoplusflares(self):
        ULT = ULTFactory(
            num_flares="2-3",
            freq_flares="two or more",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Indicated"

    def test_calculator_twoplusflares_oneflareperyear(self):
        ULT = ULTFactory(
            num_flares="2-3",
            freq_flares="one",
            ckd=CKDFactory(value=False, dialysis=False),
            erosions=ErosionsFactory(value=False),
            stones=UrateKidneyStonesFactory(value=False),
            hyperuricemia=HyperuricemiaFactory(value=False),
            tophi=TophiFactory(value=False),
        )
        assert ULT.calculator() == "Conditional"
