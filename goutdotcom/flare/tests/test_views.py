from django.test import RequestFactory, TestCase
from django.urls import reverse

from ...lab.tests.factories import UrateFactory
from ...profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)
from ...users.tests.factories import UserFactory
from ..forms import FlareForm
from ..models import Flare
from ..tests.factories import FlareFactory
from ..views import FlareCreate


class TestCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(username="bumblyboy")
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.flare_data = {
            "user": self.user,
            "monoarticular": True,
            "male": True,
            "prior_gout": True,
            "onset": True,
            "redness": True,
            "firstmtp": True,
            "location": "Left first MTP",
            "hypertension": self.user.medicalprofile.hypertension,
            "heartattack": self.user.medicalprofile.heartattack,
            "CHF": self.user.medicalprofile.CHF,
            "stroke": self.user.medicalprofile.stroke,
            "PVD": self.user.medicalprofile.PVD,
            "urate": UrateFactory(user=self.user),
            "treatment": "Ibuprofen",
        }

    def test_form_valid(self):
        form = FlareForm(data=self.flare_data)
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        # Test that user can be assigned to form instance
        self.assertEqual(form.instance.user, self.user)

    def test_get_context_data(self):
        request = self.factory.get("/flare/create")
        request.user = self.user
        response = FlareCreate.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn("hypertension_form", response.context_data)
        self.assertIn("heartattack_form", response.context_data)
        self.assertIn("CHF_form", response.context_data)
        self.assertIn("stroke_form", response.context_data)
        self.assertIn("PVD_form", response.context_data)
