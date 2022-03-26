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
        assert self.user.baselinealt.value == 78
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

    def test_remove_transaminitis_baseline_calculated(self):
        """
        Test remove_transaminitis method.
        In setting of calculated BaselineALT/AST
        Deletes BaselineALT/AST for User.
        Sets User's Transaminitis value to False
        """
        # Transaminitis = True, BaselineALT = None
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.alt1 = ALTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=300),
        )
        assert self.alt1.remove_transaminitis() == False
        # Transaminitis = True, BaselineALT created/modified after
        # ALT2 calling remove_ckd()
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.baselinealt1 = BaselineALTFactory(
            user=self.user,
            value=133,
            calculated=True,
        )
        self.alt2 = ALTFactory(
            user=self.user,
            value=133,
            date_drawn=timezone.now() - timedelta(days=290),
        )
        assert self.alt2.remove_transaminitis() == False
        assert self.user.transaminitis.value == False
        assert hasattr(self.user, "baselinealt") == False
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.baselinealt2 = BaselineALTFactory(
            user=self.user,
            value=134,
            calculated=True,
        )
        self.alt3 = ALTFactory(
            user=self.user,
            value=134,
            date_drawn=timezone.now() - timedelta(days=290),
        )
        self.ast3 = ASTFactory(
            user=self.user,
            value=134,
            date_drawn=timezone.now() - timedelta(days=290),
            alt=self.alt3,
        )
        assert self.alt3.remove_transaminitis() == False
        assert self.user.transaminitis.value == False
        assert hasattr(self.user, "baselinealt") == False
        assert hasattr(self.user, "baselineast") == False

    def test_remove_transaminitis_baseline_not_calculated(self):
        """
        Test remove_transaminitis method.
        In setting of User-defined transaminitis, BaselineALT/AST.calculated == False.
        Deletes BaselineALT/AST for User.
        Sets User's Transaminitis value to False
        """
        # Transaminitis = True, BaselineALT = None
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.alt1 = ALTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=300),
        )
        assert self.alt1.remove_transaminitis() == False
        # Transaminitis = True, BaselineALT created/modified after
        # ALT2 calling remove_ckd()
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.baselinealt1 = BaselineALTFactory(
            user=self.user,
            value=133,
            calculated=False,
        )
        self.alt2 = ALTFactory(
            user=self.user,
            value=133,
            date_drawn=timezone.now() - timedelta(days=290),
        )
        assert self.alt2.remove_transaminitis() == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselinealt
        # ALT3 date_drawn after BaselineALT created/modified
        # remove_transaminitis() remove transaminitis, delete BaselineALT
        self.alt3 = ALTFactory(
            user=self.user,
            value=133,
            date_drawn=timezone.now() + timedelta(days=290),
        )
        assert self.alt3.remove_transaminitis(alt=self.alt2) == True
        assert self.alt3.remove_transaminitis() == False
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == False
        assert hasattr(self.user, "baselinealt") == False
        # Create BaselineALT and BaselineAST, both calculated = False
        self.user.transaminitis.value = True
        self.baselinealt1 = BaselineALTFactory(
            user=self.user,
            value=133,
            calculated=False,
        )
        self.baselineast1 = BaselineASTFactory(
            user=self.user,
            value=133,
            calculated=False,
        )
        self.user.transaminitis.baseline_alt = self.baselinealt1
        self.user.transaminitis.baseline_ast = self.baselineast1
        self.user.transaminitis.save()
        assert self.alt2.remove_transaminitis() == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselinealt
        assert self.alt3.remove_transaminitis(alt=self.alt2) == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselinealt
        assert self.alt3.remove_transaminitis() == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselineast
        # BaselineALT should have been deleted via alt3.remove_transaminitis()
        assert hasattr(self.user, "baselinealt") == False
        # Create 2nd AST, associated with 2nd ALT created/modified prior to BaselineALT/AST
        self.ast2 = ASTFactory(
            user=self.user, value=133, date_drawn=timezone.now() - timedelta(days=290), alt=self.alt2
        )
        assert self.alt2.remove_transaminitis() == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselineast
        assert self.alt3.remove_transaminitis(alt=self.alt2) == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselineast
        # Create 3rd AST, created/modified after BaselineALT/AST
        self.ast3 = ASTFactory(
            user=self.user, value=133, date_drawn=timezone.now() + timedelta(days=290), alt=self.alt3
        )
        # remove_transaminitis with arg alt=self.alt2 should still evaluate to True / fail
        # Because self.alt2 and self.ast2 still older than baseline ALT/AST
        assert self.alt3.remove_transaminitis(alt=self.alt2) == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselineast
        assert self.alt3.remove_transaminitis() == False
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == False
        assert hasattr(self.user, "baselinealt") == False
        assert hasattr(self.user, "baselineast") == False

    def test_diagnose_transaminitis(self):
        """Simple test of diagnose_transaminitis method
        Simple scenarios
        """
        # Set up User with transaminitis = False
        self.user.transaminitis.value = False
        self.user.transaminitis.save()
        # Create normal ALT, disant past
        self.alt1 = ALTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        # Test that user doesn't get diagnosed with transaminitis
        # Returns False via remove_transaminitis
        assert self.alt1.diagnose_transaminitis() == False
        assert self.user.transaminitis.value == False
        # Create 2nd ALT, abnormal
        self.alt2 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=500),
        )
        # Test that user doesn't get diagnosed with transaminitis
        assert self.alt2.diagnose_transaminitis() == False
        assert self.user.transaminitis.value == False
        # Create 3rd abnormal ALT
        self.alt3 = ALTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=200),
        )
        # Test that user does get diagnosed with transaminitis
        # 2 abnormal ALTs > 6 months apart
        assert self.alt3.diagnose_transaminitis() == True
        assert self.user.transaminitis.value == True
        assert hasattr(self.user, "baselinealt") == True
        assert self.user.baselinealt.calculated == True
        # Create 4th ALT, normal value
        self.alt4 = ALTFactory(
            user=self.user,
            value=22,
            date_drawn=timezone.now() - timedelta(days=100),
        )
        # Test that User still gets diagnosed with transaminitis
        # No AST to assure GoutHelper LFTs are totally normal
        assert self.alt3.diagnose_transaminitis() == True
        assert self.user.transaminitis.value == True
        assert hasattr(self.user, "baselinealt") == True
        assert self.user.baselinealt.calculated == True
        # Create normal AST with alt = 4th ALT
        self.ast4 = ASTFactory(
            user=self.user,
            value=22,
            date_drawn=timezone.now() - timedelta(days=100),
            alt=self.alt4,
        )
        # ALT4 should now register True for normal_lfts()
        assert self.alt4.normal_lfts() == True
        assert hasattr(self.user, "baselineast") == False
        assert self.alt4.diagnose_transaminitis() == False
        assert hasattr(self.user, "baselinealt") == False
        assert hasattr(self.user, "baselineast") == False

    def test_process_high_no_baseline(self):
        """
        Test abnormal_high() method
        No baseline transaminitis or BaselineALT
        """
        # Set up User with transaminitis = False
        self.user.transaminitis.value = False
        self.user.transaminitis.save()
        # Create normal ALT, disant past
        self.alt1 = ALTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        assert self.alt1.process_high() == None
        # Create trivially high ALT
        # Check that it processes correctly (None = no alert)
        self.alt2 = ALTFactory(
            user=self.user,
            value=67,
            date_drawn=timezone.now() - timedelta(days=828),
        )
        assert self.alt2.high == True
        assert self.alt2.process_high() == None
        # Create nonurgently high ALT, check that is processes correctly
        self.alt3 = ALTFactory(
            user=self.user,
            value=111,
            date_drawn=timezone.now() - timedelta(days=788),
        )
        assert self.alt3.process_high() == "nonurgent"
        # Create typical F/U ALT, set ALT3 to abnormal_followup
        # Value of F/U ALT is normal
        self.alt4 = ALTFactory(
            user=self.user,
            value=45,
            date_drawn=timezone.now() - timedelta(days=768),
            abnormal_followup=self.alt3,
        )
        assert self.alt4.process_high() == "improving_restart"
        self.alt5 = ALTFactory(
            user=self.user,
            value=211,
            date_drawn=timezone.now() - timedelta(days=708),
        )
        assert self.alt5.process_high() == "urgent"
        assert self.alt5.flag == 3
        assert hasattr(self.user, "baselinealt") == False
        assert self.user.transaminitis.value == False
        self.alt6 = ALTFactory(
            user=self.user,
            value=145,
            date_drawn=timezone.now() - timedelta(days=468),
            abnormal_followup=self.alt5,
        )
        assert self.alt6.process_high() == "improving_recheck"
        # self.alt6.diagnose_transaminitis()
        assert hasattr(self.user, "baselinealt") == False
        self.alt7 = ALTFactory(
            user=self.user,
            value=115,
            date_drawn=timezone.now() - timedelta(days=350),
        )
        assert self.alt7.process_high() == "nonurgent"

    def test_process_high_with_baseline(self):
        """
        Test abnormal_high() method
        With baseline transaminitis or BaselineALT
        """
        # Set up User with transaminitis = False
        self.user.transaminitis.value = True
        self.baselinealt = BaselineALTFactory(
            user=self.user,
            value=133,
            calculated=False,
        )
        self.user.transaminitis.baseline_alt = self.baselinealt
        self.user.transaminitis.save()
        # Create high ALT but within the range of the User's BaselineALT
        self.alt1 = ALTFactory(
            user=self.user,
            value=98,
            date_drawn=timezone.now() - timedelta(days=343),
        )
        assert self.alt1.process_high() == None
        self.alt2 = ALTFactory(
            user=self.user,
            value=105,
            date_drawn=timezone.now() - timedelta(days=243),
        )
        assert self.alt2.process_high() == None
        assert self.user.baselinealt.value == 133
        self.alt3 = ALTFactory(
            user=self.user,
            value=555,
            date_drawn=timezone.now() + timedelta(days=2),
        )
        assert self.alt3.process_high() == "urgent"
        assert self.user.baselinealt.value == 133
        self.alt4 = ALTFactory(
            user=self.user,
            value=122,
            date_drawn=timezone.now() + timedelta(days=16),
            abnormal_followup=self.alt3,
        )
        assert self.alt4.process_high() == "improving_restart"
        assert self.user.baselinealt.value == 133


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

    def test_get_ALT(self):
        """Test getting ALT in various scenarios"""
        # Simple 1:1
        self.alt1 = ALTFactory(user=self.user, value=39, date_drawn=timezone.now() - timedelta(days=365))
        self.ast1 = ASTFactory(
            user=self.user,
            value=37,
            date_drawn=timezone.now() - timedelta(days=365),
            alt=self.alt1,
        )
        assert self.ast1.get_ALT() == self.alt1
        self.alt2 = ALTFactory(user=self.user, value=57, date_drawn=timezone.now() - timedelta(days=365))
        self.ast2 = ASTFactory(
            user=self.user,
            value=66,
            date_drawn=timezone.now() - timedelta(days=365),
            alt=self.alt2,
        )
        assert self.ast2.get_ALT() == self.alt2
        # Test returning None when there is no ALT
        self.ast3 = ASTFactory(
            user=self.user,
            value=66,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.ast3.get_ALT() == None
        # Test return ALT when AST is a abnormal_followup
        self.ast4 = ASTFactory(
            user=self.user,
            value=66,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.ast5 = ASTFactory(
            user=self.user,
            value=43,
            date_drawn=timezone.now() - timedelta(days=379),
            abnormal_followup=self.ast4,
        )
        # Check if get_ALT() returns None before 1to1 ALT created
        assert self.ast4.get_ALT() == None
        assert self.ast5.get_ALT() == None
        # Create 1to1 ALT and assign to AST
        self.alt4 = ALTFactory(user=self.user, value=57, date_drawn=timezone.now() - timedelta(days=365))
        self.ast4.alt = self.alt4
        self.ast4.save()
        assert self.ast4.get_ALT() == self.alt4
        assert self.ast5.get_ALT() == self.alt4

    def test_normal_lfts(self):
        """
        Testing test_normal_lfts() method under various scenarios
        """
        # Check for normal LFTs
        self.alt1 = ALTFactory(user=self.user, value=39, date_drawn=timezone.now() - timedelta(days=365))
        self.ast1 = ASTFactory(
            user=self.user,
            value=37,
            date_drawn=timezone.now() - timedelta(days=365),
            alt=self.alt1,
        )
        assert self.ast1.normal_lfts() == True
        # Check for abnormal LFTs
        self.alt2 = ALTFactory(user=self.user, value=57, date_drawn=timezone.now() - timedelta(days=365))
        self.ast2 = ASTFactory(
            user=self.user,
            value=66,
            date_drawn=timezone.now() - timedelta(days=365),
            alt=self.alt2,
        )
        assert self.ast2.normal_lfts() == False
        # Check for high ALT, normal AST
        self.alt3 = ALTFactory(user=self.user, value=57, date_drawn=timezone.now() - timedelta(days=365))
        self.ast3 = ASTFactory(
            user=self.user,
            value=32,
            date_drawn=timezone.now() - timedelta(days=365),
            alt=self.alt3,
        )
        assert self.ast3.normal_lfts() == False
        # Check for very high ALT/AST
        self.alt4 = ALTFactory(user=self.user, value=277, date_drawn=timezone.now() - timedelta(days=365))
        self.ast4 = ASTFactory(
            user=self.user,
            value=566,
            date_drawn=timezone.now() - timedelta(days=365),
            alt=self.alt4,
        )

        assert self.ast4.normal_lfts() == False
        # Check for a normal AST without a confirmed normal ALT
        self.ast5 = ASTFactory(
            user=self.user,
            value=26,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.ast5.normal_lfts() == False

    def test_get_baseline(self):
        """
        Testing get_baseline() method to fetch User's BaselineAST
        """
        self.alt1 = ALTFactory(user=self.user, value=39, date_drawn=timezone.now() - timedelta(days=365))
        self.ast1 = ASTFactory(
            user=self.user,
            value=37,
            date_drawn=timezone.now() - timedelta(days=365),
            alt=self.alt1,
        )
        assert self.ast1.get_baseline() == None
        self.baseline = BaselineASTFactory(
            user=self.user,
            value=37,
        )
        assert self.ast1.get_baseline() == self.baseline

    def test_get_baseline_ALT(self):
        """
        Test get_baseline_ALT() method to get AST's associated ALT.
        """
        self.alt1 = ALTFactory(user=self.user, value=39, date_drawn=timezone.now() - timedelta(days=365))
        self.ast1 = ASTFactory(
            user=self.user,
            value=37,
            date_drawn=timezone.now() - timedelta(days=365),
            alt=self.alt1,
        )
        self.baselineALT = BaselineALTFactory(
            user=self.user,
            value=37,
        )
        assert self.ast1.get_baseline_ALT() == self.baselineALT

    def test_set_baseline_one_threexhigh_AST(self):
        """
        Test set_baseline() method with single AST which is 3x the ULN
        """
        self.ast1 = ASTFactory(
            user=self.user,
            value=788,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.ast1.get_baseline() == None
        self.ast1.set_baseline()
        assert self.ast1.get_baseline() == None

    def test_set_baseline_no_initial_baseline(self):
        """
        Test set_baseline() method with single AST, no BaselineAST
        """
        self.ast1 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        assert self.ast1.get_baseline() == None
        self.ast1.set_baseline()
        assert self.ast1.get_baseline() == self.user.baselineast
        assert self.user.baselineast.value == 78

    def test_set_baseline_single_ast_initial_baseline_false(self):
        """
        Test set_baseline() method with single AST
        Baseline is set by User (calculated=False by default)
        Thus should set_baseline() should not change BaselineAST
        """
        self.ast1 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=(timezone.now() + timedelta(days=3)),
        )
        self.user.baselineast = BaselineASTFactory(
            user=self.user,
            value=98,
        )
        assert self.ast1.get_baseline() == self.user.baselineast
        self.ast1.set_baseline()
        assert self.ast1.get_baseline() == self.user.baselineast
        assert self.user.baselineast.value == 98
        assert self.user.transaminitis.value == True

    def test_set_baseline_single_ast_initial_baseline_true(self):
        """
        Test set_baseline() method with a single AST, preexisting BaselineAST
        BaselineAST is calculated
        Thus should be overwritten by set_baseline()
        """
        self.ast1 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=365),
        )
        self.user.transaminitis.value = True
        self.user.baselineast = BaselineASTFactory(
            user=self.user,
            value=98,
            calculated=True,
        )
        assert self.ast1.get_baseline() == self.user.baselineast
        self.ast1.set_baseline()
        assert self.ast1.get_baseline() == self.user.baselineast
        assert self.user.baselineast.value == 78
        assert self.user.transaminitis.last_modified == "Behind the scenes"

    def test_set_baseline_multiple_ast_no_initial_baseline(self):
        """
        Test set_baseline() method with multiples ASTs, no preexisting BaselineAST
        """
        # Create very distant AST
        # Greater than 2 years in past, won't be used for Baseline
        self.ast1 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        self.ast1.set_baseline()
        assert hasattr(self.user, "baselineast") == False
        # Create high AST within 2 years prior
        # Will be used to set baseline
        self.ast2 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=530),
        )
        self.ast2.set_baseline()
        assert self.user.baselineast.value == 78
        assert self.user.transaminitis.value == True
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        assert self.user.transaminitis.baseline_ast == self.user.baselineast
        # Create very high AST
        # Greater than 3x the upper limit of normal, won't be used for calculating BaselineAST
        self.ast3 = ASTFactory(
            user=self.user,
            value=777,
            date_drawn=timezone.now() - timedelta(days=300),
        )
        # Create another very high AST, won't be used for calculating BaselineAST
        self.ast4 = ASTFactory(
            user=self.user,
            value=7777,
            date_drawn=timezone.now() - timedelta(days=232),
        )
        self.ast4.set_baseline()
        assert self.user.baselineast.value == 78
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        # Create high AST, not > 3x ULN, will be used for calculating BaselineAST
        self.ast5 = ASTFactory(
            user=self.user,
            value=98,
            date_drawn=timezone.now() - timedelta(days=132),
        )
        self.ast5.set_baseline()
        # BaselineAST should be set to 98 because it was drawn in the last 6 months
        # Won't look back farther to 1 or 2 years, thus avoids prior ASTs for calculation
        assert self.user.baselineast.value == 98

    def test_set_baseline_multiple_ast_with_initial_baseline_calculated_false(self):
        """
        Test set_baseline() method with multiple ASTs, User-set initial BaselineAST
        BaselineAST won't be modified by set_baseline() due to calculated=False
        """
        # Create high AST, no BaselineAST created yet
        # Initial AST is > 2 years prior, won't be used for setting BaselineAST
        self.ast1 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        self.ast1.set_baseline()
        assert hasattr(self.user, "baselineast") == False
        self.ast1andahalf = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=722),
        )
        self.ast1andahalf.set_baseline()
        assert hasattr(self.user, "baselineast") == True
        assert self.user.baselineast.calculated == True
        assert self.user.baselineast.value == 78
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        # Set User's BaselineAST value and set calculated to False, then save()
        # set_baseline() should not change BaselineAST due to calculated=False
        self.user.baselineast.value = 95
        self.user.baselineast.calculated = False
        self.user.baselineast.save()
        self.user.transaminitis.last_modified = "MedicalProfile"
        self.user.transaminitis.save()
        assert self.user.transaminitis.value == True
        self.ast1.set_baseline()
        assert self.user.baselineast.value == 95
        assert self.user.transaminitis.last_modified == "MedicalProfile"
        # Create second AST that is high
        # Still won't allow set_baseline() due to calculated=False
        self.ast2 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=530),
        )
        self.ast2.set_baseline()
        assert hasattr(self.user, "baselineast") == True
        assert self.user.baselineast.value == 95
        assert self.user.transaminitis.last_modified == "MedicalProfile"

    def test_remove_transaminitis_baseline_calculated(self):
        """
        Test remove_transaminitis method.
        In setting of calculated BaselineALT/AST
        Deletes BaselineALT/AST for User.
        Sets User's Transaminitis value to False
        """
        # Transaminitis = True, BaselineAST = None
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.ast1 = ASTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=300),
        )
        assert self.ast1.remove_transaminitis() == False
        assert self.user.transaminitis.baseline_ast == None
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        assert hasattr(self.user, "baselineast") == False
        # Transaminitis = True, BaselineAST created/modified after
        # AST2 calling remove_ckd()
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.baselineast1 = BaselineASTFactory(
            user=self.user,
            value=133,
            calculated=True,
        )
        self.ast2 = ASTFactory(
            user=self.user,
            value=133,
            date_drawn=timezone.now() - timedelta(days=290),
        )
        assert self.ast2.remove_transaminitis() == False
        assert self.user.transaminitis.value == False
        assert self.user.transaminitis.baseline_ast == None
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        assert hasattr(self.user, "baselineast") == False
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.baselineast2 = BaselineASTFactory(
            user=self.user,
            value=134,
            calculated=True,
        )
        self.alt3 = ALTFactory(
            user=self.user,
            value=134,
            date_drawn=timezone.now() - timedelta(days=290),
        )
        self.ast3 = ASTFactory(
            user=self.user,
            value=134,
            date_drawn=timezone.now() - timedelta(days=290),
            alt=self.alt3,
        )
        assert self.ast3.remove_transaminitis() == False
        assert self.user.transaminitis.value == False
        assert self.user.transaminitis.baseline_ast == None
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        assert hasattr(self.user, "baselinealt") == False
        assert hasattr(self.user, "baselineast") == False

    def test_remove_transaminitis_baseline_not_calculated(self):
        """
        Test remove_transaminitis method.
        In setting of User-defined transaminitis, BaselineALT/AST.calculated == False.
        Deletes BaselineALT/AST for User.
        Sets User's Transaminitis value to False
        """
        # Transaminitis = True, BaselineAST = None
        self.user.transaminitis.value = True
        self.user.transaminitis.save()
        self.ast1 = ASTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=300),
        )
        assert self.ast1.remove_transaminitis() == False
        assert self.user.transaminitis.value == False
        assert self.user.transaminitis.baseline_ast == None
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        assert hasattr(self.user, "baselineast") == False
        # Transaminitis = True, BaselineAST created/modified after
        # AST2 calling remove_transaminitis()
        self.baselineast1 = BaselineASTFactory(
            user=self.user,
            value=133,
            calculated=False,
        )
        self.user.transaminitis.value = True
        self.user.transaminitis.last_modified = "MedicalProfile"
        self.user.transaminitis.baseline_ast = self.baselineast1
        self.user.transaminitis.save()
        self.ast2 = ASTFactory(
            user=self.user,
            value=133,
            date_drawn=timezone.now() - timedelta(days=290),
        )
        assert self.ast2.remove_transaminitis() == True
        assert self.user.transaminitis.value == True
        assert self.user.transaminitis.baseline_ast
        assert self.user.baselineast
        assert self.user.baselineast.value == 133
        # AST3 date_drawn after BaselineAST created/modified
        # remove_transaminitis() remove transaminitis, delete BaselineALT
        self.ast3 = ASTFactory(
            user=self.user,
            value=133,
            date_drawn=timezone.now() + timedelta(days=290),
        )
        assert self.ast3.remove_transaminitis(ast=self.ast2) == True
        assert self.ast3.remove_transaminitis() == False
        assert self.user.transaminitis.value == False
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        assert self.user.transaminitis.baseline_ast == None
        assert hasattr(self.user, "baselineast") == False
        # Create BaselineALT and BaselineAST, both calculated = False
        self.baselinealt1 = BaselineALTFactory(
            user=self.user,
            value=133,
            calculated=False,
        )
        self.baselineast1 = BaselineASTFactory(
            user=self.user,
            value=133,
            calculated=False,
        )
        self.user.transaminitis.value = True
        self.user.transaminitis.baseline_alt = self.baselinealt1
        self.user.transaminitis.baseline_ast = self.baselineast1
        self.user.transaminitis.last_modified = "MedicalProfile"
        self.user.transaminitis.save()
        assert self.ast2.remove_transaminitis() == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselineast
        assert self.ast3.remove_transaminitis(ast=self.ast2) == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert self.user.baselineast
        assert self.ast3.remove_transaminitis() == True
        self.user.refresh_from_db()
        # Transaminitis should still be True because BaselineALT is still present
        assert self.user.transaminitis.value == True
        # BaselineAST should have not have been deleted via ast3.remove_transaminitis()
        assert hasattr(self.user, "baselineast") == False
        assert hasattr(self.user, "baselinealt") == True
        # Create 2nd AST, associated with 2nd ALT created/modified prior to BaselineALT/AST
        self.alt2 = ALTFactory(user=self.user, value=133, date_drawn=timezone.now() - timedelta(days=290))
        self.ast2.alt = self.alt2
        self.ast2.save()
        assert self.ast2.remove_transaminitis() == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert hasattr(self.user, "baselineast") == False
        assert hasattr(self.user, "baselinealt") == True
        assert self.ast3.remove_transaminitis(ast=self.ast2) == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert hasattr(self.user, "baselineast") == False
        assert hasattr(self.user, "baselinealt") == True
        # Create 3rd ALT, created/modified after BaselineALT/AST
        self.alt3 = ALTFactory(user=self.user, value=133, date_drawn=timezone.now() + timedelta(days=290))
        self.ast3.alt = self.alt3
        self.ast3.save()
        # remove_transaminitis with arg ast=self.ast2 should still evaluate to True / fail
        # Because self.ast2 and self.alt2 still older than baseline ALT/AST
        assert self.ast3.remove_transaminitis(ast=self.ast2) == True
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == True
        assert hasattr(self.user, "baselineast") == False
        assert hasattr(self.user, "baselinealt") == True
        # remove_transaminitis called on ast3 should now return False, delete related fields
        assert self.ast3.remove_transaminitis() == False
        self.user.refresh_from_db()
        assert self.user.transaminitis.value == False
        assert self.user.transaminitis.baseline_ast == None
        assert self.user.transaminitis.baseline_alt == None
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        assert hasattr(self.user, "baselinealt") == False
        assert hasattr(self.user, "baselineast") == False

    def test_diagnose_transaminitis(self):
        """
        Test of diagnose_transaminitis() method
        Simple scenarios
        """
        # Set up User with transaminitis = False
        self.user.transaminitis.value = False
        self.user.transaminitis.save()
        # Create normal ALT, disant past
        self.ast1 = ASTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        # Test that user doesn't get diagnosed with transaminitis
        assert self.ast1.diagnose_transaminitis() == False
        assert self.user.transaminitis.value == False
        # Create 2nd AST, abnormal
        self.ast2 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=500),
        )
        # Test that user doesn't get diagnosed with transaminitis
        assert self.ast2.diagnose_transaminitis() == False
        assert self.user.transaminitis.value == False
        # Create 3rd abnormal AST
        self.ast3 = ASTFactory(
            user=self.user,
            value=78,
            date_drawn=timezone.now() - timedelta(days=200),
        )
        # Test that user does get diagnosed with transaminitis
        # Last 2 abnormal ASTs > 6 months apart
        assert self.ast3.diagnose_transaminitis() == True
        assert self.user.transaminitis.value == True
        assert hasattr(self.user, "baselineast") == True
        assert self.user.transaminitis.baseline_ast
        assert self.user.baselineast.calculated == True
        # Create 4th AST, normal value
        self.ast4 = ASTFactory(
            user=self.user,
            value=22,
            date_drawn=timezone.now() - timedelta(days=100),
        )
        # Test that User still gets diagnosed with transaminitis
        # No ALT to assure GoutHelper LFTs are totally normal
        assert self.ast4.diagnose_transaminitis() == True
        assert self.user.transaminitis.value == True
        assert hasattr(self.user, "baselineast") == True
        assert self.user.baselineast.calculated == True
        # Create normal ALT with ast4.alt = ALT
        self.alt4 = ALTFactory(
            user=self.user,
            value=22,
            date_drawn=timezone.now() - timedelta(days=100),
        )
        self.ast4.alt = self.alt4
        self.ast4.save()
        # AST4 should now register True for normal_lfts()
        assert self.ast4.normal_lfts() == True
        assert hasattr(self.user, "baselinealt") == False
        assert self.ast4.diagnose_transaminitis() == False
        assert hasattr(self.user, "baselinealt") == False
        assert hasattr(self.user, "baselineast") == False
        assert self.user.transaminitis.baseline_ast == None

    def test_process_high_no_baseline(self):
        """
        Test process_high() method
        No baseline transaminitis or BaselineAST
        """
        # Set up User with transaminitis = False
        self.user.transaminitis.value = False
        self.user.transaminitis.save()
        # Create normal AST, disant past
        self.ast1 = ASTFactory(
            user=self.user,
            value=33,
            date_drawn=timezone.now() - timedelta(days=888),
        )
        assert self.ast1.process_high() == None
        # Create trivially high AST
        # Check that it processes correctly (None = no alert)
        self.ast2 = ASTFactory(
            user=self.user,
            value=67,
            date_drawn=timezone.now() - timedelta(days=828),
        )
        assert self.ast2.high == True
        assert self.ast2.process_high() == None
        # Create nonurgently high AST, check that is processes correctly
        self.ast3 = ASTFactory(
            user=self.user,
            value=111,
            date_drawn=timezone.now() - timedelta(days=788),
        )
        assert self.ast3.process_high() == "nonurgent"
        # Create typical F/U AST, set AST3 to abnormal_followup
        # Value of F/U AST is normal
        self.ast4 = ASTFactory(
            user=self.user,
            value=45,
            date_drawn=timezone.now() - timedelta(days=768),
            abnormal_followup=self.ast3,
        )
        assert self.ast4.process_high() == "improving_restart"
        # Create abnormal AST within last 2 years
        self.ast5 = ASTFactory(
            user=self.user,
            value=311,
            date_drawn=timezone.now() - timedelta(days=708),
        )
        assert self.ast5.process_high() == "emergency"
        assert hasattr(self.user, "baselineast") == False
        assert self.user.transaminitis.value == False
        # Another abnormal high AST within last 2 years
        self.ast6 = ASTFactory(
            user=self.user,
            value=110,
            date_drawn=timezone.now() - timedelta(days=468),
            abnormal_followup=self.ast5,
        )
        assert self.ast6.process_high() == "improving_restart"
        assert hasattr(self.user, "baselineast") == True
        assert self.user.transaminitis.value == True
        assert self.user.transaminitis.last_modified == "Behind the scenes"
        assert self.user.transaminitis.baseline_ast == self.user.baselineast
        assert self.user.transaminitis.baseline_ast.value == 110

    def test_process_high_with_baseline(self):
        """
        Test abnormal_high() method
        With baseline transaminitis or BaselineAST
        """
        # Set up User with transaminitis = False
        self.user.transaminitis.value = True
        self.baselineast = BaselineASTFactory(
            user=self.user,
            value=133,
            calculated=False,
        )
        self.user.transaminitis.baseline_ast = self.baselineast
        self.user.transaminitis.save()
        # Create high ALT but within the range of the User's BaselineAST
        self.ast1 = ASTFactory(
            user=self.user,
            value=98,
            date_drawn=timezone.now() - timedelta(days=343),
        )
        assert self.ast1.process_high() == None
        self.ast2 = ASTFactory(
            user=self.user,
            value=105,
            date_drawn=timezone.now() - timedelta(days=243),
        )
        # Check that BaselineAST value isn't changing with multiple ASTs prior
        assert self.ast2.process_high() == None
        assert self.user.baselineast.value == 133
        # Create very high AST drawn after BaselineAST
        self.ast3 = ASTFactory(
            user=self.user,
            value=555,
            date_drawn=timezone.now() + timedelta(days=2),
        )
        assert self.ast3.process_high() == "urgent"
        assert self.user.baselineast.value == 133
        # Create F/U AST
        self.ast4 = ASTFactory(
            user=self.user,
            value=122,
            date_drawn=timezone.now() + timedelta(days=16),
            abnormal_followup=self.ast3,
        )
        # F/U AST should flag as improving_restart in process_high()
        assert self.ast4.process_high() == "improving_restart"
        # Should also not change the User-set baseline
        assert self.user.baselineast.value == 133


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
