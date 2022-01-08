from datetime import datetime
from decimal import *

import pytest

from goutdotcom.lab.tests.factories import LabCheckFactory

from ...profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
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
        self.labcheck = LabCheckFactory(
            user=self.user, ultplan=self.ULTPlan, due=datetime.today(), completed=True, completed_date=datetime.today()
        )
        assert self.ULTPlan.labcheck_due() == False
