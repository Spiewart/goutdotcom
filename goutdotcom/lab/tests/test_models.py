from datetime import datetime, timedelta
from decimal import *
from statistics import mean

import pytest
from django.test import Client, TestCase
from django.utils import timezone

client = Client()

from ...history.tests.factories import CKDFactory
from ...lab.models import *
from ...profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)
from ...users.tests.factories import UserFactory
from .factories import (
    ALTFactory,
    ASTFactory,
    BaselineALTFactory,
    BaselineASTFactory,
    BaselineCreatinineFactory,
    CreatinineFactory,
    HemoglobinFactory,
    PlateletFactory,
    UrateFactory,
    WBCFactory,
)

pytestmark = pytest.mark.django_db

### HAVE NOT FIGURED OUT HOW TO TEST GET_ABSOLUTE_URL
### PATIENTPROVIDERMIXIN REQUIRES REQUEST TO ACCESS VIEW
### I THINK REVERSE IN GET_ABSOLUTE_URL USES VIEW


class TestRoundDecimal:
    def test_value_return(self):
        value = Decimal(0.59343)
        assert value.quantize(Decimal(10) ** -2) == Decimal("0.59")


class TestUrateMethods(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = PatientProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.client.force_login(self.user)

    def test__str__(self):
        urate = UrateFactory(user=self.user)
        assert urate.__str__() == "urate " + str(urate.value) + " mg/dL (milligrams per deciliter)"

    def test__unicode__(self):
        urate = UrateFactory(user=self.user)
        assert urate.__unicode__() == str(urate.name)


class TestALTMethods(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = PatientProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.client.force_login(self.user)

    def test__str__(self):
        ALT = ALTFactory(user=self.user)
        assert ALT.__str__() == "ALT " + str(ALT.value) + " U/L (units per liter)"

    def test__unicode__(self):
        ALT = ALTFactory(user=self.user)
        assert ALT.__unicode__() == str(ALT.name)

    def test_get_AST(self):
        """Test getting AST in various scenarios"""
        # Simple 1:1
        self.alt1 = ALTFactory(
            user=self.user,
            value=37,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast1 = ASTFactory(user=self.user, value=39, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt1)
        assert self.alt1.get_AST() == self.ast1
        self.alt2 = ALTFactory(
            user=self.user,
            value=66,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast2 = ASTFactory(user=self.user, value=57, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt2)
        assert self.alt2.get_AST() == self.ast2
        # Test returning None when there is no AST
        self.alt3 = ALTFactory(
            user=self.user,
            value=66,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.alt3.get_AST() == None
        # Test return AST when ALT is a abnormal_followup
        self.alt4 = ALTFactory(
            user=self.user,
            value=66,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.alt5 = ALTFactory(
            user=self.user,
            value=43,
            date_drawn=timezone.now() - timedelta(days=379),
            abnormal_followup=self.alt4,
        )
        # Check if get_AST() returns None before 1to1 AST created
        assert self.alt4.get_AST() == None
        assert self.alt5.get_AST() == None
        # Create 1to1 AST and assign to ALT
        self.ast4 = ASTFactory(user=self.user, value=57, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt4)
        assert self.alt4.get_AST() == self.ast4
        assert self.alt5.get_AST() == self.ast4

    def test_normal_lfts(self):
        self.alt1 = ALTFactory(
            user=self.user,
            value=37,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast1 = ASTFactory(user=self.user, value=39, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt1)
        assert self.alt1.normal_lfts() == True
        self.alt2 = ALTFactory(
            user=self.user,
            value=66,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast2 = ASTFactory(user=self.user, value=57, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt2)
        assert self.alt2.normal_lfts() == False
        self.alt3 = ALTFactory(
            user=self.user,
            value=32,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast3 = ASTFactory(user=self.user, value=57, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt3)
        assert self.alt3.normal_lfts() == False
        self.alt4 = ALTFactory(
            user=self.user,
            value=566,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast4 = ASTFactory(
            user=self.user, value=277, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt4
        )
        assert self.alt4.normal_lfts() == False
        self.alt5 = ALTFactory(
            user=self.user,
            value=26,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.alt5.normal_lfts() == False

    def test_get_baseline(self):
        self.alt1 = ALTFactory(
            user=self.user,
            value=37,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast1 = ASTFactory(user=self.user, value=39, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt1)
        assert self.alt1.get_baseline() == None
        self.baseline = BaselineALTFactory(
            user=self.user,
            value=37,
        )
        assert self.alt1.get_baseline() == self.baseline

    def test_get_baseline_AST(self):
        self.alt1 = ALTFactory(
            user=self.user,
            value=37,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast1 = ASTFactory(user=self.user, value=39, date_drawn=timezone.now() - timedelta(days=365), alt=self.alt1)
        assert self.alt1.get_baseline() == None
        self.baseline = BaselineALTFactory(
            user=self.user,
            value=37,
        )
        self.baselineAST = BaselineASTFactory(
            user=self.user,
            value=37,
        )
        assert self.alt1.get_baseline_AST() == self.baselineAST

    def test_set_baseline_no_initial_baseline(self):
        self.alt1 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.alt1.get_baseline() == None
        self.alt1.set_baseline()
        assert self.alt1.get_baseline() == self.user.baselinealt
        assert self.user.baselinealt.value == 78

    def test_set_baseline_single_alt_initial_baseline_false(self):
        self.alt1 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now(),
        )
        self.user.baselinealt = BaselineALTFactory(
            user=self.user,
            value=98,
        )
        assert self.alt1.get_baseline() == self.user.baselinealt
        self.alt1.set_baseline()
        self.alt1.refresh_from_db()
        assert self.alt1.get_baseline() == self.user.baselinealt
        assert self.user.baselinealt.value == 98
        assert self.user.transaminitis.value == True

    def test_set_baseline_single_alt_initial_baseline_true(self):
        self.alt1 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.user.transaminitis.value = True
        self.user.baselinealt = BaselineALTFactory(
            user=self.user,
            value=98,
            calculated=True,
        )
        assert self.alt1.get_baseline() == self.user.baselinealt
        self.alt1.set_baseline()
        self.alt1.refresh_from_db()
        assert self.alt1.get_baseline() == self.user.baselinealt
        assert self.user.baselinealt.value == 78
        assert self.user.transaminitis.last_modified == "Behind the scenes"

    def test_set_baseline_multiple_alt_no_initial_baseline(self):
        self.alt1 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        self.alt1.set_baseline()
        assert hasattr(self.user, "baselinealt") == False
        self.alt2 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=530),
        )
        self.alt1.set_baseline()
        assert self.user.baselinealt.value == 78
        self.alt3 = ALTFactory(
            user=self.user,
            value=777,
            date_drawn=timezone.now() - timedelta(days=300),
        )
        self.alt4 = ALTFactory(
            user=self.user,
            value=7777,
            date_drawn=timezone.now() - timedelta(days=232),
        )
        self.alt1.set_baseline()
        assert self.user.baselinealt.value == mean([777, 7777])
        assert self.user.transaminitis.last_modified == "Behind the scenes"

    def test_set_baseline_multiple_alt_with_initial_baseline_calculated_false(self):
        self.alt1 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        self.alt1.set_baseline()
        assert hasattr(self.user, "baselinealt") == False
        self.alt1andahalf = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=722),
        )
        self.alt1andahalf.set_baseline()
        assert hasattr(self.user, "baselinealt") == True
        assert self.user.baselinealt.calculated == True
        self.user.baselinealt.value = 95
        self.user.baselinealt.calculated = False
        self.user.baselinealt.save()
        assert self.user.transaminitis.value == True
        self.alt1.set_baseline()
        assert self.user.baselinealt.value == 95
        self.alt2 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=530),
        )
        self.alt1.set_baseline()
        assert hasattr(self.user, "baselinealt") == True
        self.alt3 = ALTFactory(
            user=self.user,
            value=777,
            date_drawn=timezone.now() - timedelta(days=300),
        )
        self.alt4 = ALTFactory(
            user=self.user,
            value=7777,
            date_drawn=timezone.now() - timedelta(days=232),
        )
        self.alt1.set_baseline()
        assert hasattr(self.user, "baselinealt") == True

    def test_diagnose_transaminitis(self):
        """Simple test of diagnose_transaminitis method
        Simple scenarios
        """
        self.user.transaminitis.value = False
        self.user.transaminitis.save()
        self.alt1 = ALTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        assert self.user.transaminitis.value == False
        self.alt2 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=500),
        )
        self.alt3 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=200),
        )
        assert self.alt3.diagnose_transaminitis() == True
        assert self.user.transaminitis.value == True
        assert self.user.baselinealt
        assert self.user.baselinealt.calculated == True
        self.alt4 = ALTFactory(
            user=self.user,
            value=22,
            date_drawn=timezone.now() - timedelta(days=100),
        )
        assert self.alt3.diagnose_transaminitis() == True
        self.ast4 = ASTFactory(
            user=self.user,
            value=22,
            date_drawn=timezone.now() - timedelta(days=100),
            alt=self.alt4,
        )
        assert self.alt4.normal_lfts() == True
        assert self.alt4.get_baseline()
        assert self.alt4.get_baseline().calculated == True
        self.alt4.refresh_from_db()
        self.alt3.refresh_from_db()
        assert self.alt4.get_baseline_AST() == None
        assert self.alt4.diagnose_transaminitis() == False
        assert self.alt3.diagnose_transaminitis() == False


class TestASTMethods(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = PatientProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.client.force_login(self.user)

    def test__str__(self):
        AST = ASTFactory(user=self.user)
        assert AST.__str__() == "AST " + str(AST.value) + " U/L (units per liter)"

    def test__unicode__(self):
        AST = ASTFactory(user=self.user)
        assert AST.__unicode__() == str(AST.name)


class TestPlateletMethods(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = PatientProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.client.force_login(self.user)

    def test__str__(self):
        platelet = PlateletFactory(user=self.user)
        assert platelet.__str__() == "platelet " + str(platelet.value) + " PLTS/\u03BCL (platelets per microliter)"

    def test__unicode__(self):
        platelet = PlateletFactory(user=self.user)
        assert platelet.__unicode__() == str(platelet.name)


class TestWBCMethods(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = PatientProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.client.force_login(self.user)

    def test__str__(self):
        WBC = WBCFactory(user=self.user)
        assert WBC.__str__() == "WBC " + str(WBC.value) + " cells/mm^3 (cells per cubic millimeter)"

    def test__unicode__(self):
        WBC = WBCFactory(user=self.user)
        assert WBC.__unicode__() == str(WBC.name)


class TestHemoglobinMethods(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = PatientProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.client.force_login(self.user)

    def test__str__(self):
        hemoglobin = HemoglobinFactory(user=self.user)
        assert hemoglobin.__str__() == "hemoglobin " + str(hemoglobin.value) + " g/dL (grams per deciliter)"

    def test__unicode__(self):
        hemoglobin = HemoglobinFactory(user=self.user)
        assert hemoglobin.__unicode__() == str(hemoglobin.name)


class TestCreatinineMethods(TestCase):
    def setUp(self):
        self.user = UserFactory(role="PATIENT")
        self.profile = PatientProfileFactory(
            user=self.user, date_of_birth=(timezone.now().date() - timedelta(weeks=(52 * 70)))
        )
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user, CKD=CKDFactory(user=self.user, value=False))
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.client.force_login(self.user)

    def test__str__(self):
        self.creatinine = CreatinineFactory(user=self.user)
        assert (
            self.creatinine.__str__()
            == "creatinine " + str(self.creatinine.value) + " mg/dL (milligrams per deciliter)"
        )

    def test__unicode__(self):
        self.creatinine = CreatinineFactory(user=self.user)
        assert self.creatinine.__unicode__() == str(self.creatinine.name)

    def test_sex_vars_kappa(self):
        self.creatinine = CreatinineFactory(user=self.user)
        if self.profile.gender == "male":
            assert self.creatinine.sex_vars_kappa() == Decimal(0.9)
        elif self.profile.gender == "female":
            assert self.creatinine.sex_vars_kappa() == Decimal(0.7)
        else:
            assert self.creatinine.eGFR_calculator().sex_vars_kappa() == False

    def test_sex_vars_alpha(self):
        self.creatinine = CreatinineFactory(user=self.user)
        if self.profile.gender == "male":
            assert self.creatinine.sex_vars_alpha() == Decimal(-0.411)
        elif self.profile.gender == "female":
            assert self.creatinine.sex_vars_alpha() == Decimal(-0.329)
        else:
            assert self.creatinine.eGFR_calculator().sex_vars_kappa() == False

    def test_race_modifier(self):
        self.creatinine = CreatinineFactory(user=self.user)
        if self.profile.race == "black":
            assert self.creatinine.race_modifier() == Decimal(1.159)
        elif (
            self.profile.race == "white"
            or self.profile.race == "asian"
            or self.profile.race == "native american"
            or self.profile.race == "hispanic"
        ):
            assert self.creatinine.race_modifier() == Decimal(1.00)
        else:
            assert self.creatinine.eGFR_calculator() == False

    def test_sex_modifier(self):
        self.creatinine = CreatinineFactory(user=self.user)
        if self.profile.gender == "male":
            assert self.creatinine.sex_modifier() == Decimal(1.018)
        elif self.profile.gender == "female" or self.profile.gender == "non-binary":
            assert self.creatinine.sex_modifier() == Decimal(1.00)
        else:
            assert self.creatinine.eGFR_calculator() == False

    def test_eGFR_calculator(self):
        self.creatinine = CreatinineFactory(user=self.user)
        ##assert Creatinine.eGFR_calculator() == "Can't calculate eGFR without an age (make a profile)"
        kappa = 0
        alpha = 0
        race = 0
        sex = 0
        age = self.profile.age

        if self.profile.gender == "male":
            sex = Decimal(1.018)
            kappa = Decimal(0.9)
            alpha = Decimal(-0.411)
        elif self.profile.gender == "female":
            sex = Decimal(1.00)
            kappa = Decimal(0.7)
            alpha = Decimal(-0.329)
        else:
            return "Something went wrong with eGFR calculation"
        if self.profile.race == "black":
            race = Decimal(1.159)
        elif (
            self.profile.race == "white"
            or self.profile.race == "asian"
            or self.profile.race == "native american"
            or self.profile.race == "hispanic"
        ):
            race = Decimal(1.00)
        else:
            return "Something went wrong with eGFR calculation"
        eGFR = (
            Decimal(141)
            * min(self.creatinine.value / kappa, Decimal(1.00)) ** alpha
            * max(self.creatinine.value / kappa, Decimal(1.00)) ** Decimal(-1.209)
            * Decimal(0.993) ** age
            * race
            * sex
        )
        assert self.creatinine.eGFR_calculator() == round_decimal(eGFR, 2)

    def test_set_baseline_no_CKD(self):
        """
        Test checking the function of set_baseline() method
        """
        self.creatinine1 = CreatinineFactory(
            user=self.user,
            value=Decimal(0.6),
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.creatinine2 = CreatinineFactory(
            user=self.user,
            value=Decimal(0.6),
            date_drawn=timezone.now() - timedelta(days=323),
        )
        self.creatinine3 = CreatinineFactory(
            user=self.user,
            value=Decimal(1.5),
            date_drawn=timezone.now() - timedelta(days=251),
        )
        self.creatinine3.set_baseline()
        assert self.user.ckd.value == True
        assert self.user.ckd.baseline
        assert self.user.ckd.baseline.value

    def test_set_baseline_single_creatinine(self):
        """
        Test checking the function of set_baseline() method
        """
        self.creatinine1 = CreatinineFactory(
            user=self.user,
            value=Decimal(2.6),
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.user.ckd.value == False
        self.creatinine1.set_baseline()
        assert self.user.ckd.value == True
        assert self.user.ckd.baseline
        assert self.user.baselinecreatinine.value
        # Need to refresh from DB when modifying object with class-based method
        # https://stackoverflow.com/questions/39779228/django-not-updating-object-in-classmethod-very-strange
        self.creatinine1.refresh_from_db()
        assert self.user.ckd.value == True
        assert self.user.baselinecreatinine.value

    def test_diagnose_CKD_with_CKD_no_baseline(self):
        """
        Test checking the function of diagnose_ckd() method
        With CKD but no User-entered baseline
        """
        self.creatinine1 = CreatinineFactory(
            user=self.user,
            value=Decimal(1.6),
            date_drawn=timezone.now() - timedelta(days=364),
        )
        assert self.creatinine1.diagnose_ckd() == False
        assert self.user.ckd.value == False
        self.creatinine2 = CreatinineFactory(
            user=self.user,
            value=Decimal(1.8),
            date_drawn=timezone.now() - timedelta(days=323),
        )
        assert self.creatinine2.diagnose_ckd() == False
        assert self.user.ckd.value == False
        self.creatinine3 = CreatinineFactory(
            user=self.user,
            value=Decimal(2.2),
            date_drawn=timezone.now() - timedelta(days=240),
        )
        assert self.creatinine3.diagnose_ckd() == True
        # Need to refresh from DB when modifying object with class-based method
        # https://stackoverflow.com/questions/39779228/django-not-updating-object-in-classmethod-very-strange
        self.user.ckd.refresh_from_db()
        self.user.baselinecreatinine.refresh_from_db()
        assert self.user.ckd.value == True
        assert self.user.ckd.baseline
        assert self.user.ckd.last_modified == "Behind the scenes"
        assert self.user.baselinecreatinine
        assert self.user.baselinecreatinine.calculated == True
        assert round(self.user.baselinecreatinine.value, 2) == round(
            mean([self.creatinine1.value, self.creatinine2.value, self.creatinine3.value]), 2
        )

    def test_diagnose_CKD_with_CKD_with_initial_baseline(self):
        """
        Test checking the function of diagnose_ckd() method
        With CKD and User-entered initial baseline
        """
        self.user.ckd.value = True
        self.user.ckd.baseline = BaselineCreatinineFactory(user=self.user, value=Decimal(1.9))
        self.user.ckd.stage = self.user.ckd.baseline.stage_calculator()
        self.user.ckd.save()
        assert self.user.ckd.value == True
        assert self.user.baselinecreatinine.value == Decimal(1.9)
        assert self.user.ckd.stage == 3 or self.user.ckd.stage == 4
        self.creatinine1 = CreatinineFactory(
            user=self.user,
            value=Decimal(1.6),
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.creatinine1.diagnose_ckd() == True
        assert self.user.ckd.value == True
        assert len(Creatinine.objects.filter(user=self.user)) == 1
        assert self.creatinine1.get_baseline().value == round(Decimal(1.9), 2)
        self.creatinine2 = CreatinineFactory(
            user=self.user,
            value=Decimal(1.8),
            date_drawn=timezone.now() - timedelta(days=323),
        )
        assert self.creatinine2.diagnose_ckd() == True
        assert self.user.ckd.value == True
        assert len(Creatinine.objects.filter(user=self.user)) == 2
        assert self.creatinine2.get_baseline().value == round(Decimal(1.9), 2)
        self.creatinine3 = CreatinineFactory(
            user=self.user,
            value=Decimal(2.2),
            date_drawn=timezone.now() - timedelta(days=240),
        )
        assert self.creatinine3.diagnose_ckd() == True
        # Need to refresh from DB when modifying object with class-based method
        # https://stackoverflow.com/questions/39779228/django-not-updating-object-in-classmethod-very-strange
        self.user.ckd.refresh_from_db()
        self.user.baselinecreatinine.refresh_from_db()
        assert self.user.ckd.value == True
        assert self.user.ckd.baseline
        assert self.user.baselinecreatinine
        assert self.creatinine3.get_baseline().value == round(Decimal(1.9), 2)
        # Create Creatinine in normal range dated BEFORE today
        # User's BaselineCreatinine was created today
        # To test remove_ckd(), shouldn't remove User's Baseline
        self.creatinine4 = CreatinineFactory(
            user=self.user,
            value=Decimal(0.75),
            date_drawn=timezone.now() - timedelta(days=8),
        )
        assert self.creatinine4.date_drawn < self.user.baselinecreatinine.modified
        assert self.creatinine4.diagnose_ckd() == True
        self.user.ckd.refresh_from_db()
        assert self.user.ckd.value == True
        assert self.user.ckd.baseline
        assert self.user.baselinecreatinine
        # Create Creatinine in normal range dated AFTER today
        # User's BaselineCreatinine was created today
        # To test remove_ckd(), should remove User's Baseline
        self.creatinine5 = CreatinineFactory(
            user=self.user,
            value=Decimal(0.75),
            date_drawn=timezone.now() + timedelta(days=50),
        )
        assert self.creatinine5.date_drawn > self.user.baselinecreatinine.modified
        assert self.creatinine5.diagnose_ckd() == False
        self.user.ckd.refresh_from_db()
        assert self.user.ckd.value == False
        assert self.user.ckd.baseline == None
        assert self.user.ckd.last_modified == "Behind the scenes"
        assert self.user.baselinecreatinine.DoesNotExist

    def test_diagnose_CKD_without_initial_CKD(self):
        """
        Test checking the function of diagnose_CKD() method
        Without CKD initially but developing
        """
        self.creatinine1 = CreatinineFactory(
            user=self.user,
            value=Decimal(0.6),
            date_drawn=timezone.now() - timedelta(days=700),
        )
        assert self.creatinine1.diagnose_ckd() == False
        assert self.user.ckd.value == False
        self.creatinine2 = CreatinineFactory(
            user=self.user,
            value=Decimal(0.9),
            date_drawn=timezone.now() - timedelta(days=550),
        )
        assert self.creatinine2.diagnose_ckd() == False
        assert self.creatinine2.get_baseline() == None
        self.creatinine3 = CreatinineFactory(
            user=self.user,
            value=Decimal(3.6),
            date_drawn=timezone.now() - timedelta(days=400),
        )
        assert self.creatinine3.diagnose_ckd() == False
        assert self.creatinine3.get_baseline() == None
        self.creatinine4 = CreatinineFactory(
            user=self.user,
            value=Decimal(2.3),
            date_drawn=timezone.now() - timedelta(days=370),
        )
        assert self.creatinine4.diagnose_ckd() == False
        assert self.creatinine4.get_baseline() == None
        self.creatinine5 = CreatinineFactory(
            user=self.user,
            value=Decimal(2.2),
            date_drawn=timezone.now() - timedelta(days=350),
        )
        assert self.creatinine5.diagnose_ckd() == False
        assert self.creatinine5.get_baseline() == None
        self.creatinine6 = CreatinineFactory(
            user=self.user,
            value=Decimal(2.9),
            date_drawn=timezone.now() - timedelta(days=305),
        )
        assert self.creatinine6.diagnose_ckd() == True
        # Need to refresh from DB when modifying object with class-based method
        # https://stackoverflow.com/questions/39779228/django-not-updating-object-in-classmethod-very-strange
        self.creatinine6.refresh_from_db()
        self.user.ckd.refresh_from_db()
        assert self.creatinine6.get_baseline()
        assert self.user.baselinecreatinine.value

    def test_process_high_no_CKD(self):
        """
        Test checking the function of process_high() method
        Without CKD initially
        """
        self.creatinine1 = CreatinineFactory(
            user=self.user,
            value=Decimal(0.75),
            date_drawn=timezone.now() - timedelta(days=700),
        )
        assert self.creatinine1.abnormal == None
        self.creatinine2 = CreatinineFactory(
            user=self.user,
            value=Decimal(0.9),
            date_drawn=timezone.now() - timedelta(days=550),
        )
        assert self.creatinine2.abnormal == None
        self.creatinine3 = CreatinineFactory(
            user=self.user,
            value=Decimal(1.9),
            date_drawn=timezone.now() - timedelta(days=400),
        )
        assert self.creatinine3.abnormal == "H"
        assert self.creatinine3.var_x_high(1.5) == False
        assert self.creatinine3.var_x_high(1.25) == True
        assert self.creatinine3.process_high() == "nonurgent"
