from datetime import datetime, timedelta
from decimal import *

import pytest

from ...history.tests.factories import CKDFactory
from ...lab.tests.factories import (
    ALTFactory,
    ASTFactory,
    CreatinineFactory,
    HemoglobinFactory,
    LabCheckFactory,
    PlateletFactory,
    UrateFactory,
    WBCFactory,
)
from ...profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)
from ...treatment.choices import QDAY
from ...treatment.tests.factories import (
    AllopurinolFactory,
    ColchicineFactory,
    FebuxostatFactory,
)
from ...users.tests.factories import UserFactory
from .factories import ULTPlanFactory

pytestmark = pytest.mark.django_db


class TestULTPlanMethods:
    def test_get_absolute_url(self):
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ULTPlan = ULTPlanFactory(user=self.user)
        assert self.ULTPlan.get_absolute_url() == f"/ultplan/{self.ULTPlan.pk}/"

    def test_labcheck_due_no_labcheck(self):
        """Test that checks if the ULTPlan has a LabCheck due when there is no LabCheck logged, such as immediately after creating a ULTPlan"""
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=100, goal_urate=6.0, titrating=True, last_titration=None
        )
        assert self.ULTPlan.labcheck_due() == True
        assert self.ULTPlan.last_labcheck() == None

    def test_labcheck_due_initial_labcheck(self):
        """Test that checks if the ULTPlan has a LabCheck due when there is one LabCheck logged the same day as the creation of the ULTPlan"""
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=100, goal_urate=6.0, titrating=True, last_titration=None
        )
        self.labcheck1 = LabCheckFactory(
            user=self.user, ultplan=self.ULTPlan, due=datetime.today(), completed=True, completed_date=datetime.today()
        )
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            due=(datetime.today() + timedelta(days=42)),
            completed=False,
            completed_date=None,
        )
        assert self.ULTPlan.labcheck_due() == False
        assert self.ULTPlan.last_labcheck() == self.labcheck2

    ### REWRITE THIS
    def test_labcheck_due_second_labcheck_due(self):
        """Test that checks if the ULTPlan's second LabCheck, which is due, triggers labcheck_due()=True."""
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=100, goal_urate=6.0, titrating=True, last_titration=None
        )
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            due=(datetime.today() - timedelta(days=42)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=42)),
        )
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            due=(datetime.today()),
            completed=False,
            completed_date=None,
        )
        assert self.ULTPlan.labcheck_due() == True
        assert self.ULTPlan.last_labcheck() == self.labcheck2

    def test_labcheck_due_second_labcheck_done(self):
        """Test that checks if the ULTPlan's second LabCheck, which is done, triggers labcheck_due()=False."""
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=100, goal_urate=6.0, titrating=True, last_titration=None
        )
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            due=(datetime.today() - timedelta(days=42)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=42)),
        )
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            due=datetime.today(),
            completed=True,
            completed_date=datetime.today(),
        )
        self.labcheck3 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            due=(datetime.today() + timedelta(days=42)),
            completed=False,
            completed_date=None,
        )
        assert self.ULTPlan.labcheck_due() == False
        assert self.ULTPlan.last_labcheck() == self.labcheck3

    def test_titrate_allopurinol(self):
        """Test that checks if the ULTPlan's titrate() returns correctly under a variety of scenarios."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=100, goal_urate=6.0, titrating=True, last_titration=None
        )
        # Create Allopurinol for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.allopurinol = AllopurinolFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=100,
            freq=QDAY,
            # Set date_started to 6 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=42)),
            side_effects=None,
            de_sensitized=None,
        )
        # Create uncompleted initial LabCheck due = 6 weeks prior
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=42)),
            completed=False,
            completed_date=None,
        )
        # Check that titrate returns False because LabCheck is not complete
        assert self.ULTPlan.titrate(self.labcheck1) == False
        # Switch first LabCheck to completed = True
        self.labcheck1.completed = True
        self.labcheck1.completed_date = datetime.today() - timedelta(days=42)
        # Need to save LabCheck after modifying attributes...
        self.labcheck1.save()
        # Check that titrate() still returns False because there is only 1 LabCheck associated with the ULTPlan (initial)
        assert self.ULTPlan.titrate(self.labcheck1) == False
        # Create second LabCheck due = the day of creation
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            # Specify Urate fields to trigger titration with high urate value
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            due=(datetime.today()),
            completed=False,
            completed_date=None,
        )
        # Check that titration() returns False because last LabCheck is not completed
        assert self.ULTPlan.titrate(self.labcheck2) == False
        # Switch labcheck2.completed to = True, titrate() should evaluate to True because there is > 1 LabCheck for the ULTPlan and the urate was set to 14.5
        self.labcheck2.completed = True
        self.labcheck2.completed_date = datetime.today()
        # Need to save LabCheck after modifying attributes
        self.labcheck2.save()
        assert self.ULTPlan.titrate(self.labcheck2) == True
        # Check that Allopurinol dose was correctly increased by titrate()
        assert self.allopurinol.dose == 200

    def test_titrate_febuxostat(self):
        """Test that checks if the ULTPlan's titrate() returns correctly under a variety of additional scenarios and with febuostat instead of allopurinol."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=False,
            completed_date=None,
        )
        # Check that titrate returns False because LabCheck is not complete
        assert self.ULTPlan.titrate(self.labcheck1) == False
        # Switch first LabCheck to completed = True
        self.labcheck1.completed = True
        self.labcheck1.completed_date = datetime.today() - timedelta(days=365)
        # Need to save LabCheck after modifying attributes...
        self.labcheck1.save()
        # Check that titrate() still returns False because there is only 1 LabCheck associated with the ULTPlan (initial)
        assert self.ULTPlan.titrate(self.labcheck1) == False
        # Create second LabCheck due = the day of creation
        self.labcheck2 = self.ULTPlan.labcheck_set.last()
        self.labcheck2.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck2.due = datetime.today() - timedelta(days=323)
        self.labcheck2.completed = False
        self.labcheck2.completed_date = None
        self.labcheck2.save()
        # Check that titration() returns False because last LabCheck is not completed
        assert self.ULTPlan.titrate(self.labcheck2) == False
        assert self.febuxostat.dose == 20
        assert self.colchicine.dose == 0.6
        # Switch labcheck2.completed to = True, titrate() should evaluate to True because there is > 1 LabCheck for the ULTPlan and the urate was set to 14.5
        self.labcheck2.completed = True
        self.labcheck2.completed_date = datetime.today() - timedelta(days=323)
        # Need to save LabCheck after modifying attributes...
        self.labcheck2.save()
        assert self.ULTPlan.titrate(self.labcheck2) == True
        # Check that Febuxostat dose was correctly increased by titrate()
        assert self.febuxostat.dose == 40
        assert self.colchicine.dose == 0.6
        # Check that ULTPlan last_titration set to today()
        assert self.ULTPlan.last_titration == datetime.today().date()
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=9.5)
        self.labcheck3.due = datetime.today() - timedelta(days=270)
        self.labcheck3.completed = False
        self.labcheck3.completed_date = None
        self.labcheck3.save()
        # Check that titration() returns False because last LabCheck is not completed
        assert self.ULTPlan.titrate(self.labcheck3) == False
        # Switch labcheck3.completed to = True, titrate() should evaluate to True because there is > 1 LabCheck for the ULTPlan and the urate was set to 9.5
        self.labcheck3.completed = True
        self.labcheck3.completed_date = datetime.today() - timedelta(days=270)
        # Need to save LabCheck after modifying attributes...
        self.labcheck3.save()
        assert self.ULTPlan.titrate(self.labcheck3) == True
        # Check that Febuxostat dose was correctly increased by titrate()
        assert self.febuxostat.dose == 60
        assert self.colchicine.dose == 0.6
        # Check that ULTPlan last_titration set to today()
        assert self.ULTPlan.last_titration == datetime.today().date()
        self.labcheck4 = self.ULTPlan.labcheck_set.last()
        self.labcheck4.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=4.5)
        self.labcheck4.due = datetime.today() - timedelta(days=200)
        self.labcheck4.completed = True
        self.labcheck4.completed_date = datetime.today() - timedelta(days=200)
        self.labcheck4.save()
        # labcheck4.titrate() should evaluate to False because, while the urate is under goal_urate, it has not been so for 6 months or longer (six_months_at_goal() returns False)
        assert self.ULTPlan.titrate(self.labcheck4) == False
        # Febuxostat dose should have not been titrated up because Urate was at goal
        assert self.febuxostat.dose == 60
        assert self.colchicine.dose == 0.6
        # labcheck5.titrate() should evaluate to True because there is > 1 LabCheck for the ULTPlan and the urate was set to 4.5 (under goal) and has been so for > 6 months
        self.labcheck5 = self.ULTPlan.labcheck_set.last()
        self.labcheck5.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=4.8)
        self.labcheck5.due = datetime.today().date()
        self.labcheck5.completed = True
        self.labcheck5.completed_date = datetime.today().date()
        self.labcheck5.save()
        assert self.ULTPlan.titrate(self.labcheck5) == True
        assert self.febuxostat.dose == 60
        assert self.colchicine.dose == 0.6
        assert self.colchicine.prophylaxis_finished == True
        assert self.colchicine.date_ended == datetime.today().date()
        assert self.ULTPlan.titrating == False
        # Subsequent Labcheck6 6 months into the future where the urate isn't at goal
        # Check that ULTPlan and related models reflect moving back into titration
        self.labcheck6 = self.ULTPlan.labcheck_set.last()
        self.labcheck6.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=7.5)
        self.labcheck6.due = due = datetime.today() + timedelta(days=180)
        self.labcheck6.completed = True
        self.labcheck6.completed_date = due = datetime.today() + timedelta(days=180)
        self.labcheck6.save()
        assert self.ULTPlan.titrate(self.labcheck6) == True
        assert self.febuxostat.dose == 80
        assert self.colchicine.dose == 0.6
        assert self.colchicine.prophylaxis_finished == False
        assert self.colchicine.date_ended == None
        assert self.ULTPlan.titrating == True

    def test_abnormal_alt(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly.
        Using ALT under a variety of scenarios."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.8),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=False,
            completed_date=None,
        )
        # Check that check_for_abnormal_labs returns None because LabCheck is not complete
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck1) == None
        # Switch first LabCheck to completed = True
        self.labcheck1.completed = True
        self.labcheck1.completed_date = datetime.today() - timedelta(days=365)
        # Need to save LabCheck after modifying attributes...
        self.labcheck1.save()
        # Check that check_for_abnormal_labs() still returns False
        # Because there is only 1 LabCheck with no abnormal labs
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck1) == False
        # Create second LabCheck 42 days after initial LabCheck
        # This would be typical for starting ULT and checking labs 6 weeks later
        # ALT is markedly elevated above the reference range
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=340),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.8),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=11.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=323)),
        )
        # check_for_abnormal_labs() should evaluate to True because the ALT is elevated > 3x the upper limit of normal
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck2) == True
        # ULTPlan should be "paused" after calling check_abnormal_labs() with the high ALT
        assert self.ULTPlan.pause == True
        # ULT for ULTPLan should have active set to False while figuring out what's wrong with the ALT
        assert self.ULTPlan.get_ult().active == False
        # PPx for ULTPlan should also have active set to False while figuring out what's wrong with the ALT
        assert self.ULTPlan.get_ppx().active == False
        # Check that newly created LabCheck is set to not completed (False)
        assert self.ULTPlan.labcheck_set.last().completed == False
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck2
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (datetime.today() - timedelta(days=323) + self.ULTPlan.urgent_lab_interval).date()
        )

    def test_abnormal_creatinine_normal_baseline(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly.
        Using Creatinine which is initially within normal limits."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=1.0),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=365)).date(),
        )
        # Create second LabCheck 42 days after initial LabCheck
        # This would be typical for starting ULT and checking labs 6 weeks later
        # Creatinine is slightly elevated above the reference range (< 1.5x)
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=1.6),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=11.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=323)).date(),
        )
        # check_for_abnormal_labs() should evaluate to True because the Creatinine is elevated
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck2) == True
        # ULTPlan should NOT BE "paused" after calling check_abnormal_labs() with the high Creatinine being <= 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True while figuring out what's wrong with the ALT
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True while figuring out what's wrong with the ALT
        assert self.ULTPlan.get_ppx().active == True
        # Check that newly created LabCheck is set to not completed (False)
        assert self.ULTPlan.labcheck_set.last().completed == False
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck2
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (datetime.today() - timedelta(days=323) + self.ULTPlan.urgent_lab_interval).date()
        )
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck3
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        # Check that labcheck3 abnormal_labcheck is set to labcheck2, which created most recent LabCheck
        assert self.labcheck3.abnormal_labcheck == self.labcheck2
        # Assign lab values to labcheck3, including critically high creatinine value
        self.labcheck3.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck3.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=33)
        self.labcheck3.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=3.6)
        self.labcheck3.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=333)
        self.labcheck3.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Mark labcheck3 as completed, with date, and save()
        self.labcheck3.completed = True
        self.labcheck3.completed_date = (
            datetime.today() - timedelta(days=323) + self.ULTPlan.urgent_lab_interval
        ).date()
        self.labcheck3.save()
        # check_for_abnormal_labs() should evaluate to True because the Creatinine is elevated
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck3) == True
        # ULTPlan SHOULD BE "paused" after calling check_abnormal_labs() with the high Creatinine being > 2x the upper limit of normal
        assert self.ULTPlan.pause == True
        # ULT for ULTPLan should have active set to False while figuring out what's wrong with the Creatinine
        assert self.ULTPlan.get_ult().active == False
        # PPx for ULTPlan should also have active set to False while figuring out what's wrong with the Creatinine
        assert self.ULTPlan.get_ppx().active == False

    def test_abnormal_creatinine_CKD_baseline(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly.
        User has CKD at baseline."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user, CKD=CKDFactory(user=self.user, value=True))
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=2.2),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=365)).date(),
        )
        # Create second LabCheck 42 days after initial LabCheck
        # This would be typical for starting ULT and checking labs 6 weeks later
        # Creatinine is slightly elevated above the reference range (< 1.5x)
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=2.5),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=11.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=323)).date(),
        )
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck2)
        # ULTPlan should NOT BE "paused" after calling check_abnormal_labs() with the high Creatinine being <= 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True while figuring out what's wrong with the Creatinine
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True while figuring out what's wrong with the Creatinine
        assert self.ULTPlan.get_ppx().active == True
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck3
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        # Set third LabCheck to LabCheck created by 42 days after second LabCheck
        # This would be typical for continuing ULT with a reassuring 2nd LabCheck and checking labs 6 weeks later
        # Creatinine is > 1.25 x above the baseline
        self.labcheck3.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck3.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck3.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=3.2)
        self.labcheck3.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222)
        self.labcheck3.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.completed = True
        self.labcheck3.completed_date = (
            datetime.today() - timedelta(days=323) + self.ULTPlan.titration_lab_interval
        ).date()
        self.labcheck3.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck3)
        # ULTPlan SHOULD NOT BE "paused" after calling check_abnormal_labs() with the high Creatinine being < 1.5x the baseline
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True because the Creatinine elevation isn't > 1.5x
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True because the Creatinine elevation isn't > 1.5x
        assert self.ULTPlan.get_ppx().active == True
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck3
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (
                datetime.today()
                - timedelta(days=323)
                + self.ULTPlan.titration_lab_interval
                + self.ULTPlan.urgent_lab_interval
            ).date()
        )
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck4
        self.labcheck4 = self.ULTPlan.labcheck_set.last()
        # Check that labcheck3 abnormal_labcheck is set to labcheck2, which created most recent LabCheck
        assert self.labcheck4.abnormal_labcheck == self.labcheck3
        # Assign lab values to labcheck4, including critically high creatinine value
        self.labcheck4.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck4.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=33)
        self.labcheck4.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=5.5)
        self.labcheck4.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck4.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=333)
        self.labcheck4.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck4.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Mark labcheck4 as completed, with date, and save()
        self.labcheck4.completed = True
        self.labcheck4.completed_date = (
            datetime.today()
            - timedelta(days=323)
            + self.ULTPlan.titration_lab_interval
            + self.ULTPlan.urgent_lab_interval
        ).date()
        self.labcheck4.save()
        # check_for_abnormal_labs() should evaluate to True because the Creatinine is elevated
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck4) == True
        # ULTPlan SHOULD BE "paused" after calling check_abnormal_labs() with the high Creatinine being > 2x the upper limit of normal
        assert self.ULTPlan.pause == True
        # ULT for ULTPLan should have active set to False while figuring out what's wrong with the Creatinine
        assert self.ULTPlan.get_ult().active == False
        # PPx for ULTPlan should also have active set to False while figuring out what's wrong with the Creatinine
        assert self.ULTPlan.get_ppx().active == False

    def test_abnormal_creatinine_twoinarow_nonurgent_CKD_baseline(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly.
        User has CKD at baseline."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user, CKD=CKDFactory(user=self.user, value=True))
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=2.2),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=365)).date(),
        )
        # Create second LabCheck 42 days after initial LabCheck
        # This would be typical for starting ULT and checking labs 6 weeks later
        # Creatinine is slightly elevated above the reference range (< 1.5x)
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=2.5),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=11.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=True,
            completed_date=(datetime.today().date() - timedelta(days=323)),
        )
        # check_for_abnormal_labs() should evaluate to False because the Creatinine is elevated but not far enough off the patient's baseline (initial LabCheck) to matter
        self.ULTPlan.check_for_abnormal_labs(self.labcheck2)
        # ULTPlan should NOT BE "paused" after calling check_abnormal_labs() with the high Creatinine being <= 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True while figuring out what's wrong with the Creatinine
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True while figuring out what's wrong with the Creatinine
        assert self.ULTPlan.get_ppx().active == True
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck3
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        # Create third LabCheck 42 days after second LabCheck
        # This would be typical for continuing ULT with a reassuring 2nd LabCheck and checking labs 6 weeks later
        # Creatinine is > 1.25 x above the baseline
        self.labcheck3.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck3.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck3.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=3.2)
        self.labcheck3.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222)
        self.labcheck3.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.completed = True
        self.labcheck3.completed_date = (
            datetime.today() - timedelta(days=323) + self.ULTPlan.titration_lab_interval
        ).date()
        self.labcheck3.save()
        # check_for_abnormal_labs() should evaluate to True because the Creatinine is elevated > 1.25 x the baseline
        self.ULTPlan.check_for_abnormal_labs(self.labcheck3)
        # ULTPlan SHOULD NOT BE "paused" after calling check_abnormal_labs() with the high Creatinine being < 1.5x the baseline
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True because the Creatinine elevation isn't > 1.5x
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True because the Creatinine elevation isn't > 1.5x
        assert self.ULTPlan.get_ppx().active == True
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck3
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (
                datetime.today()
                - timedelta(days=323)
                + self.ULTPlan.titration_lab_interval
                + self.ULTPlan.urgent_lab_interval
            ).date()
        )
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck4
        self.labcheck4 = self.ULTPlan.labcheck_set.last()
        # Check that labcheck3 abnormal_labcheck is set to labcheck2, which created most recent LabCheck
        assert self.labcheck4.abnormal_labcheck == self.labcheck3
        # Assign lab values to labcheck4, including a second non-urgently high creatinine value
        self.labcheck4.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck4.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=33)
        self.labcheck4.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=2.9)
        self.labcheck4.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck4.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=333)
        self.labcheck4.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck4.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Mark labcheck4 as completed, with date, and save()
        self.labcheck4.completed = True
        self.labcheck4.completed_date = (
            datetime.today()
            - timedelta(days=323)
            + self.ULTPlan.titration_lab_interval
            + self.ULTPlan.urgent_lab_interval
        ).date()
        self.labcheck4.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck4)
        print(self.labcheck4.abnormal_labcheck)
        print(self.labcheck4)
        # ULTPlan SHOULD NOT BE "paused" after calling check_abnormal_labs() with the high Creatinine being > 1.5x < 2x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True because Creatinine didn't change that much
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True because Creatinine didn't change that much
        assert self.ULTPlan.get_ppx().active == True
        print(self.ULTPlan.titrating)
        print(self.ULTPlan.labcheck_set.last().abnormal_labcheck)
        print(self.ULTPlan.labcheck_set.last())
        assert self.ULTPlan.labcheck_set.last().due == (
            self.labcheck4.completed_date + self.ULTPlan.titration_lab_interval - self.ULTPlan.urgent_lab_interval
        )

    def test_abnormal_platelet_high_baseline_normal(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly.
        User has normal platelets at baseline."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.9),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=222),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=365)),
        )
        # Create second LabCheck 42 days after initial LabCheck
        # This would be typical for starting ULT and checking labs 6 weeks later
        # Platelet is slightly elevated above the reference range (< 1.5x)
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.8),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=466),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=11.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=323)),
        )
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck2)
        # ULTPlan should NOT BE "paused" after calling check_abnormal_labs() with the high Platelet being <= 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ppx().active == True
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck3
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        # This would be typical for continuing ULT with a reassuring 2nd LabCheck and checking labs 6 weeks later
        self.labcheck3.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck3.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck3.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.7)
        self.labcheck3.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Assign Platelet value that is > 1.5x the upper limit of normal to labcheck3.platelet
        self.labcheck3.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=677)
        self.labcheck3.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.completed = True
        self.labcheck3.completed_date = (
            datetime.today() - timedelta(days=323) + self.ULTPlan.titration_lab_interval
        ).date()
        self.labcheck3.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck3)
        # ULTPlan SHOULD NOT BE "paused" after calling check_abnormal_labs() with the first high Platelet being > 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True still because its only the first high Platelet
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True still because its only the first high Platelet
        assert self.ULTPlan.get_ppx().active == True
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck3
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (
                datetime.today()
                - timedelta(days=323)
                + self.ULTPlan.titration_lab_interval
                + self.ULTPlan.urgent_lab_interval
            ).date()
        )
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck4
        self.labcheck4 = self.ULTPlan.labcheck_set.last()
        # Check that labcheck4 abnormal_labcheck is set to labcheck3, which created most recent LabCheck
        assert self.labcheck4.abnormal_labcheck == self.labcheck3
        # Assign lab values to labcheck4, including second critically high platelet value
        self.labcheck4.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck4.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=33)
        self.labcheck4.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.9)
        self.labcheck4.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck4.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=700)
        self.labcheck4.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck4.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Mark labcheck4 as completed, with date, and save()
        self.labcheck4.completed = True
        self.labcheck4.completed_date = (
            datetime.today()
            - timedelta(days=323)
            + self.ULTPlan.titration_lab_interval
            + self.ULTPlan.urgent_lab_interval
        ).date()
        self.labcheck4.save()
        # check_for_abnormal_labs() should evaluate to True because the Platelet is elevated critically elevated for the second time in a row and the initial value was normal
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck4) == True
        # ULTPlan SHOULD BE "paused" after calling check_abnormal_labs()
        assert self.ULTPlan.pause == True
        # ULT for ULTPLan should have active set to False
        assert self.ULTPlan.get_ult().active == False
        # PPx for ULTPlan should also have active set to False
        assert self.ULTPlan.get_ppx().active == False

    def test_abnormal_platelet_high_baseline_low(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly.
        User has low platelets at baseline."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.9),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=105),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=365)),
        )
        # Create second LabCheck 42 days after initial LabCheck
        # This would be typical for starting ULT and checking labs 6 weeks later
        # Platelet is slightly elevated above the reference range (< 1.5x)
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.8),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=466),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=11.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=323)),
        )
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck2)
        # ULTPlan should NOT BE "paused" after calling check_abnormal_labs() with the high Platelet being <= 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ppx().active == True
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck3
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        # This would be typical for continuing ULT with a reassuring 2nd LabCheck and checking labs 6 weeks later
        self.labcheck3.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck3.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck3.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.7)
        self.labcheck3.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Assign Platelet value that is > 1.5x the upper limit of normal to labcheck3.platelet
        self.labcheck3.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=677)
        self.labcheck3.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.completed = True
        self.labcheck3.completed_date = (
            datetime.today() - timedelta(days=323) + self.ULTPlan.titration_lab_interval
        ).date()
        self.labcheck3.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck3)
        # ULTPlan SHOULD NOT BE "paused" after calling check_abnormal_labs() with the first high Platelet being > 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True still because its only the first high Platelet
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True still because its only the first high Platelet
        assert self.ULTPlan.get_ppx().active == True
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck3
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (
                datetime.today()
                - timedelta(days=323)
                + self.ULTPlan.titration_lab_interval
                + self.ULTPlan.urgent_lab_interval
            ).date()
        )
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck4
        self.labcheck4 = self.ULTPlan.labcheck_set.last()
        # Check that labcheck4 abnormal_labcheck is set to labcheck3, which created most recent LabCheck
        assert self.labcheck4.abnormal_labcheck == self.labcheck3
        # Assign lab values to labcheck4, including second critically high platelet value
        self.labcheck4.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck4.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=33)
        self.labcheck4.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.9)
        self.labcheck4.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck4.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=700)
        self.labcheck4.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck4.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Mark labcheck4 as completed, with date, and save()
        self.labcheck4.completed = True
        self.labcheck4.completed_date = (
            datetime.today()
            - timedelta(days=323)
            + self.ULTPlan.titration_lab_interval
            + self.ULTPlan.urgent_lab_interval
        ).date()
        self.labcheck4.save()
        # check_for_abnormal_labs() should evaluate to True because the Platelet is elevated critically elevated for the second time in a row and the initial value was normal
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck4) == True
        # ULTPlan SHOULD BE "paused" after calling check_abnormal_labs()
        assert self.ULTPlan.pause == True
        # ULT for ULTPLan should have active set to False
        assert self.ULTPlan.get_ult().active == False
        # PPx for ULTPlan should also have active set to False
        assert self.ULTPlan.get_ppx().active == False

    def test_abnormal_platelet_high_baseline_high(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly.
        User has high platelets at baseline."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.9),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            # Baseline platelet value is above the upper limit of normal, indicating some sort of thrombocytosis
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=510),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=365)),
        )
        # Create second LabCheck 42 days after initial LabCheck
        # This would be typical for starting ULT and checking labs 6 weeks later
        # Platelet is slightly elevated above the reference range (< 1.5x)
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.8),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=466),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=11.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=323)),
        )
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck2)
        # ULTPlan should NOT BE "paused" after calling check_abnormal_labs() with the high Platelet being <= 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ppx().active == True
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck3
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        # This would be typical for continuing ULT with a reassuring 2nd LabCheck and checking labs 6 weeks later
        self.labcheck3.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck3.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck3.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.7)
        self.labcheck3.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Assign Platelet value that is > 1.5x the upper limit of normal to labcheck3.platelet
        self.labcheck3.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=677)
        self.labcheck3.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.completed = True
        self.labcheck3.completed_date = (
            datetime.today() - timedelta(days=323) + self.ULTPlan.titration_lab_interval
        ).date()
        self.labcheck3.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck3)
        # ULTPlan SHOULD NOT BE "paused" after calling check_abnormal_labs() with the first high Platelet being > 1.5x the upper limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True still because its only the first high Platelet
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True still because its only the first high Platelet
        assert self.ULTPlan.get_ppx().active == True
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck3
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (
                datetime.today()
                - timedelta(days=323)
                + self.ULTPlan.titration_lab_interval
                + self.ULTPlan.urgent_lab_interval
            ).date()
        )
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck4
        self.labcheck4 = self.ULTPlan.labcheck_set.last()
        # Check that labcheck4 abnormal_labcheck is set to labcheck3, which created most recent LabCheck
        assert self.labcheck4.abnormal_labcheck == self.labcheck3
        # Assign lab values to labcheck4, including second critically high platelet value
        self.labcheck4.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck4.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=33)
        self.labcheck4.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.9)
        self.labcheck4.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck4.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=700)
        self.labcheck4.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck4.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Mark labcheck4 as completed, with date, and save()
        self.labcheck4.completed = True
        self.labcheck4.completed_date = (
            datetime.today()
            - timedelta(days=323)
            + self.ULTPlan.titration_lab_interval
            + self.ULTPlan.urgent_lab_interval
        ).date()
        self.labcheck4.save()
        # check_for_abnormal_labs() should evaluate to False because the Platelet is elevated at baseline and has been ever since (average of all Platelet values > 1.1x the upper limit of normal)
        assert self.ULTPlan.check_for_abnormal_labs(self.labcheck4) == True
        # ULTPlan SHOULD NOT BE "paused" after calling check_abnormal_labs()
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True
        assert self.ULTPlan.get_ppx().active == True

    def test_abnormal_platelet_low_baseline_normal(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly for low platelets.
        User has normal platelets at baseline."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.9),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            # Normal baseline platelets
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=250),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=365)),
        )
        # Create second LabCheck 42 days after initial LabCheck
        # This would be typical for starting ULT and checking labs 6 weeks later
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.8),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            # Platelet is lower than the lower limit of normal reference range (150K)
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=124),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=11.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=323)),
        )
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck2)
        # ULTPlan should NOT BE "paused" after calling check_abnormal_labs() with the high Platelet being > 50% the lower limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ppx().active == True
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck3
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        # Check that labcheck3's due date is set to the urgent_lab_interval into the future
        assert self.labcheck3.due == (datetime.today() - timedelta(days=323) + self.ULTPlan.urgent_lab_interval).date()
        self.labcheck3.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck3.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck3.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.7)
        self.labcheck3.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Platelet value is again lower than the reference range, this time < 75% of the lower limit of normal
        self.labcheck3.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=78)
        self.labcheck3.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.completed = True
        self.labcheck3.completed_date = (
            datetime.today() - timedelta(days=323) + self.ULTPlan.urgent_lab_interval
        ).date()
        self.labcheck3.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck3)
        # ULTPlan SHOULD BE "paused" after calling check_abnormal_labs() because it is the second abnormal in a row, this one being < 75% the lower limit of normal, and the baseline is normal
        assert self.ULTPlan.pause == True
        # ULT for ULTPLan should have active set to False
        assert self.ULTPlan.get_ult().active == False
        # PPx for ULTPlan should also have active set to False
        assert self.ULTPlan.get_ppx().active == False
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck3
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (
                datetime.today()
                - timedelta(days=323)
                + self.ULTPlan.urgent_lab_interval
                + self.ULTPlan.urgent_lab_interval
            ).date()
        )

    def test_abnormal_platelet_low_baseline_low(self):
        """Test that checks if the ULTPlan's check_for_abnormal_labs() returns correctly for low platelets.
        User has low platelets at baseline."""
        # Set up User with required Profile objects
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        # Create ULTPlan for User, specify fields that would typically be created by ULTAid
        self.ULTPlan = ULTPlanFactory(
            user=self.user, dose_adjustment=20, goal_urate=5.0, titrating=True, last_titration=None
        )
        # Create Febuxostat for User and ULTplan, would also typically be created at creation of ULTPlan but by view
        self.febuxostat = FebuxostatFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=20,
            freq=QDAY,
            # Set date_started to 52 weeks prior for to check titration() function correctly
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        self.colchicine = ColchicineFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            dose=0.6,
            freq=QDAY,
            prn=False,
            as_prophylaxis=True,
            date_started=(datetime.today() - timedelta(days=365)),
            side_effects=None,
        )
        # Create uncompleted initial LabCheck due = 52 weeks prior, needs to be created when it would typically be created by the ULTPlanCreate view
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            alt=ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34),
            ast=ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32),
            creatinine=CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.9),
            hemoglobin=HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            # Low baseline platelets
            platelet=PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=123),
            wbc=WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3),
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5),
            due=(datetime.today() - timedelta(days=365)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=365)).date(),
        )
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck1)
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck1
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck2
        self.labcheck2 = self.ULTPlan.labcheck_set.last()
        # Create second LabCheck urgent_lab_interval days after the intial because the first Platelet level was low
        # This would be typical for starting ULT with an initial low Platelet
        self.labcheck2.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck2.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck2.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.8)
        self.labcheck2.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Platelet is lower than the lower limit of normal reference range (150K)
        self.labcheck2.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=143)
        self.labcheck2.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=9.3)
        self.labcheck2.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=17.5)
        self.labcheck2.completed = True
        self.labcheck2.completed_date = (datetime.today() - self.ULTPlan.urgent_lab_interval).date()
        self.labcheck2.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck2)
        # ULTPlan should NOT BE "paused" after calling check_abnormal_labs() with the high Platelet being > 75% the lower limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True while figuring out what's wrong with the Platelet
        assert self.ULTPlan.get_ppx().active == True
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck3
        self.labcheck3 = self.ULTPlan.labcheck_set.last()
        # Check that labcheck3's due date is set to the urgent_lab_interval into the future
        assert (
            self.labcheck3.due
            == (datetime.today() - self.ULTPlan.urgent_lab_interval + self.ULTPlan.titration_lab_interval).date()
        )
        # This would be typical for continuing ULT with a reassuring 2nd LabCheck and checking labs 6 weeks later
        self.labcheck3.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck3.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck3.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.7)
        self.labcheck3.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Platelet value is again lower than the reference range, this time < 75% of the lower limit of normal
        self.labcheck3.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=78)
        self.labcheck3.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck3.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck3.completed = True
        self.labcheck3.completed_date = (
            datetime.today() - self.ULTPlan.urgent_lab_interval + self.ULTPlan.titration_lab_interval
        ).date()
        self.labcheck3.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck3)
        # ULTPlan SHOULD NOT BE "paused" after calling check_abnormal_labs().
        # Value is < 75% the lower limit of normal, but baseline is low and it is > 50% the lower limit of normal
        assert self.ULTPlan.pause == False
        # ULT for ULTPLan should have active set to True
        assert self.ULTPlan.get_ult().active == True
        # PPx for ULTPlan should also have active set to True
        assert self.ULTPlan.get_ppx().active == True
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        # Check that a new LabCheck was created titration_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (
                datetime.today()
                - self.ULTPlan.urgent_lab_interval
                + self.ULTPlan.titration_lab_interval
                + self.ULTPlan.titration_lab_interval
            ).date()
        )
        # LabCheck created by check_for_abnormal_labs() above assigned to labcheck4
        self.labcheck4 = self.ULTPlan.labcheck_set.last()
        # Last LabCheck for this test has critically low platelet, should pause ULTPlan
        self.labcheck4.alt = ALTFactory(user=self.user, ultplan=self.ULTPlan, value=34)
        self.labcheck4.ast = ASTFactory(user=self.user, ultplan=self.ULTPlan, value=32)
        self.labcheck4.creatinine = CreatinineFactory(user=self.user, ultplan=self.ULTPlan, value=0.7)
        self.labcheck4.hemoglobin = HemoglobinFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        # Platelet value is again lower than the reference range, this time < 75% of the lower limit of normal
        self.labcheck4.platelet = PlateletFactory(user=self.user, ultplan=self.ULTPlan, value=45)
        self.labcheck4.wbc = WBCFactory(user=self.user, ultplan=self.ULTPlan, value=4.3)
        self.labcheck4.urate = UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5)
        self.labcheck4.completed = True
        self.labcheck4.completed_date = (
            datetime.today()
            - self.ULTPlan.urgent_lab_interval
            + self.ULTPlan.titration_lab_interval
            + self.ULTPlan.urgent_lab_interval
        ).date()
        self.labcheck4.save()
        # Call check_for_abnormal_labs()
        self.ULTPlan.check_for_abnormal_labs(self.labcheck4)
        # ULTPlan SHOULD BE "paused" after calling check_abnormal_labs().
        # Value is < 50% the lower limit of normal
        assert self.ULTPlan.pause == True
        # ULT for ULTPLan should have active set to False
        assert self.ULTPlan.get_ult().active == False
        # PPx for ULTPlan should also have active set to False
        assert self.ULTPlan.get_ppx().active == False
        # Check that newly created LabCheck abnormal_labcheck is set to last LabCheck, which was abnormal
        assert self.ULTPlan.labcheck_set.last().abnormal_labcheck == self.labcheck4
        # Check that a new LabCheck was created urgent_lab_interval days into the future
        assert (
            self.ULTPlan.labcheck_set.last().due
            == (
                datetime.today()
                - self.ULTPlan.urgent_lab_interval
                + self.ULTPlan.urgent_lab_interval
                + self.ULTPlan.titration_lab_interval
                + self.ULTPlan.urgent_lab_interval
            ).date()
        )
