from decimal import *

import pytest

from ...history.tests.factories import (
    AllopurinolHypersensitivityFactory,
    CKDFactory,
    FebuxostatHypersensitivityFactory,
    HeartAttackFactory,
    OrganTransplantFactory,
    StrokeFactory,
    XOIInteractionsFactory,
)
from .factories import ULTAidFactory

pytestmark = pytest.mark.django_db


class TestULTAidMethods:
    def test_get_absolute_url(self):
        ULTAid = ULTAidFactory()
        assert ULTAid.get_absolute_url() == f"/ultaid/{ULTAid.pk}/"

    def test_decision_aid_XOI_interactions(self):
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=False, dialysis=False),
            XOI_interactions=XOIInteractionsFactory(value=True),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=False),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["rheumatologist"] == True

    def test_decision_aid_organ_transplant(self):
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=False, dialysis=False),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=True),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=False),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["rheumatologist"] == True

    def test_decision_aid_CKD_4(self):
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=True, dialysis=False, stage=4),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=False),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["dose"] == "50 mg"

    def test_decision_aid_CKD_4_febuxostat(self):
        # Tests whether febuxostat dose is adjusted due to CKD.
        ## FEBUXOSTAT PICKED BY ALLOPURINOL_HYPERSENSITIVITY = TRUE
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=True, dialysis=False, stage=4),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=True),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["dose"] == "20 mg"

    def test_decision_aid_both_hypersensitivity(self):
        # Tests whether "rheumatologist" == True when hypersensitivity to both allopurinol and febuxostat present
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=False, dialysis=False),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=True),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=True),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["rheumatologist"] == True

    def test_decision_aid_allopurinol_hypersensitivity_heartattack(self):
        # Tests whether "rheumatologist" == True when hypersensitive to allopurinol and history of heart attack
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=False, dialysis=False),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=True),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=True),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["rheumatologist"] == True

    def test_decision_aid_allopurinol_hypersensitivity_stroke(self):
        # Tests whether "rheumatologist" == True when hypersensitive to allopurinol and history of stroke
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=False, dialysis=False),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=True),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=True),
        )
        assert ULTAid.decision_aid()["rheumatologist"] == True

    def test_decision_aid_allopurinol_hypersensitivity(self):
        # Tests whether febuxostat is picked in the presence of allopurinol_hypersensitivity == True
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=False, dialysis=False),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=True),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["drug"] == "febuxostat"
        assert ULTAid.decision_aid()["dose"] == "40 mg"

    def test_decision_aid_allopurinol_hypersensitivity_CKD_4(self):
        # Tests whether febuxostat is picked in the presence of allopurinol_hypersensitivity == True and that the dose is "20 mg" when CKD = True and CKD.stage > 3
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=True, dialysis=False, stage=4),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=True),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["drug"] == "febuxostat"
        assert ULTAid.decision_aid()["dose"] == "20 mg"

    def test_decision_aid_allopurinol_hypersensitivity_CKD_nostage(self):
        # Tests whether febuxostat is picked in the presence of allopurinol_hypersensitivity == True and that the dose is "20 mg" when CKD = True but no stage is recorded (safety)
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=True, dialysis=False, stage=None),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=True),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=False),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["drug"] == "febuxostat"
        assert ULTAid.decision_aid()["dose"] == "20 mg"

    def test_decision_aid_febuxostat_hypersensitivity(self):
        # Tests whether allopurinol is picked in the presence of febuxostat_hypersensitivity == True
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=False, dialysis=False),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=False),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=True),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["drug"] == "allopurinol"
        assert ULTAid.decision_aid()["dose"] == "100 mg"

    def test_decision_aid_febuxostat_hypersensitivity_CKD_4(self):
        # Tests whether allopurinol is picked in the presence of febuxostat_hypersensitivity == True and that the dose is "50 mg" when CKD = True and CKD.stage > 3
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=True, dialysis=False, stage=4),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=False),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=True),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["drug"] == "allopurinol"
        assert ULTAid.decision_aid()["dose"] == "50 mg"

    def test_decision_aid_febuxostat_hypersensitivity_CKD_no_stage(self):
        # Tests whether allopurinol is picked in the presence of febuxostat_hypersensitivity == True and that the dose is "50 mg" when CKD == True but not CKD stage is recorded (safety)
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=True, dialysis=False, stage=None),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=False),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=True),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["drug"] == "allopurinol"
        assert ULTAid.decision_aid()["dose"] == "50 mg"

    def test_decision_aid_febuxostat_hypersensitivity_CKD_2(self):
        # Tests whether allopurinol is picked in the presence of febuxostat_hypersensitivity == True and that the dose is "100 mg" when CKD == True but CKD.stage < 3
        ULTAid = ULTAidFactory(
            need=True,
            want=True,
            ckd=CKDFactory(value=True, dialysis=False, stage=2),
            XOI_interactions=XOIInteractionsFactory(value=False),
            organ_transplant=OrganTransplantFactory(value=False),
            allopurinol_hypersensitivity=AllopurinolHypersensitivityFactory(value=False),
            febuxostat_hypersensitivity=FebuxostatHypersensitivityFactory(value=True),
            heartattack=HeartAttackFactory(value=False),
            stroke=StrokeFactory(value=False),
        )
        assert ULTAid.decision_aid()["drug"] == "allopurinol"
        assert ULTAid.decision_aid()["dose"] == "100 mg"
