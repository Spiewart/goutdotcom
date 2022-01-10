from datetime import datetime, timedelta
from decimal import *

import pytest

from goutdotcom.lab.tests.factories import LabCheckFactory

from ...lab.tests.factories import UrateFactory
from ...profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)
from ...treatment.choices import QDAY
from ...treatment.tests.factories import AllopurinolFactory, FebuxostatFactory
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
            due=(datetime.today() - timedelta(days=42)),
            completed=False,
            completed_date=None,
        )
        # Check that titrate returns False because LabCheck is not complete
        assert self.ULTPlan.titrate(self.labcheck1) == False
        # Switch first LabCheck to completed = True
        self.labcheck1.completed = True
        self.labcheck1.completed_date = datetime.today() - timedelta(days=42)
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
        # Create uncompleted initial LabCheck due = 52 weeks prior
        self.labcheck1 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            due=(datetime.today() - timedelta(days=365)),
            completed=False,
            completed_date=None,
        )
        # Check that titrate returns False because LabCheck is not complete
        assert self.ULTPlan.titrate(self.labcheck1) == False
        # Switch first LabCheck to completed = True
        self.labcheck1.completed = True
        self.labcheck1.completed_date = datetime.today() - timedelta(days=365)
        # Check that titrate() still returns False because there is only 1 LabCheck associated with the ULTPlan (initial)
        assert self.ULTPlan.titrate(self.labcheck1) == False
        # Create second LabCheck due = the day of creation
        self.labcheck2 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            # Specify Urate fields to trigger titration with high urate value
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=14.5),
            due=(datetime.today() - timedelta(days=323)),
            completed=False,
            completed_date=None,
        )
        # Check that titration() returns False because last LabCheck is not completed
        assert self.ULTPlan.titrate(self.labcheck2) == False
        # Switch labcheck2.completed to = True, titrate() should evaluate to True because there is > 1 LabCheck for the ULTPlan and the urate was set to 14.5
        self.labcheck2.completed = True
        self.labcheck2.completed_date = datetime.today()
        assert self.ULTPlan.titrate(self.labcheck2) == True
        # Check that Febuxostat dose was correctly increased by titrate()
        assert self.febuxostat.dose == 40
        # Check that ULTPlan last_titration set to today()
        assert self.ULTPlan.last_titration == datetime.today().date()
        self.labcheck3 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            # Specify Urate fields to trigger titration with high urate value
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=9.5),
            due=(datetime.today() - timedelta(days=270)),
            completed=False,
            completed_date=None,
        )
        # Check that titration() returns False because last LabCheck is not completed
        assert self.ULTPlan.titrate(self.labcheck3) == False
        # Switch labcheck3.completed to = True, titrate() should evaluate to True because there is > 1 LabCheck for the ULTPlan and the urate was set to 9.5
        self.labcheck3.completed = True
        self.labcheck3.completed_date = datetime.today() - timedelta(days=270)
        assert self.ULTPlan.titrate(self.labcheck3) == True
        # Check that Febuxostat dose was correctly increased by titrate()
        assert self.febuxostat.dose == 60
        # Check that ULTPlan last_titration set to today()
        assert self.ULTPlan.last_titration == datetime.today().date()
        self.labcheck4 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            # Set urate field to under goal so titrate returns False
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=4.5),
            due=(datetime.today() - timedelta(days=200)),
            completed=True,
            completed_date=(datetime.today() - timedelta(days=200)),
        )
        # labcheck5.titrate() should evaluate to True because there is > 1 LabCheck for the ULTPlan and the urate was set to 4.5 (under goal) and has been so for > 6 months
        assert self.ULTPlan.titrate(self.labcheck4) == False
        assert self.febuxostat.dose == 60
        self.labcheck5 = LabCheckFactory(
            user=self.user,
            ultplan=self.ULTPlan,
            # Set urate field to under goal so titrate returns False
            urate=UrateFactory(user=self.user, ultplan=self.ULTPlan, value=4.8),
            due=datetime.today(),
            completed=True,
            completed_date=datetime.today(),
        )
        assert self.ULTPlan.titrate(self.labcheck5) == True
        assert self.febuxostat.dose == 60
        assert self.ULTPlan.titrating == False
