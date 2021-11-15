from decimal import *
from math import floor

import pytest

from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

from ...profiles.tests.factories import (
    FamilyProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)
from .factories import HeightFactory, WeightFactory

pytestmark = pytest.mark.django_db


class TestWeightMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        weight = WeightFactory(user=user)
        assert weight.__str__() == str(weight.value)

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        weight = WeightFactory(user=user)
        assert weight.__unicode__() == str(weight.name)

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        weight = WeightFactory(user=user)
        assert weight.get_absolute_url() == f"/vitals/weight/{weight.pk}/"

    def test_convert_pounds_to_kg(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        weight = WeightFactory(value=100, user=user)
        assert round(weight.value / 2.205, 1) == 45.4


class TestHeightMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        height = HeightFactory(user=user)
        assert height.__str__() == str(height.value)

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        height = HeightFactory(user=user)
        assert height.__unicode__() == str(height.name)

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        height = HeightFactory(user=user)
        assert height.get_absolute_url() == f"/vitals/height/{height.pk}/"

    def test_convert_inches_to_feet(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        height = HeightFactory(value=75, user=user)
        height_feet = floor(height.value / 12)
        height_inches = height.value - height_feet * 12
        assert height_feet == 6
        assert height_inches == 3
        assert height.convert_inches_to_feet() == "6 foot 3 inches"

    def test_convert_inches_to_meters(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        height = HeightFactory(value=75, user=user)
        assert round(height.value / 39.37, 2) == 1.91
