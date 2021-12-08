from django.forms.models import model_to_dict
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ...lab.forms import UrateFlareForm
from ...lab.tests.factories import UrateFactory
from ...profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)
from ...users.tests.factories import UserFactory
from ..choices import *
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
        self.urate_data = UrateFactory(user=self.user)
        self.flare_data = {
            "user": self.user,
            "monoarticular": True,
            "male": True,
            "prior_gout": True,
            "onset": True,
            "redness": True,
            "firstmtp": True,
            "location": [],
            "hypertension": self.user.medicalprofile.hypertension,
            "heartattack": self.user.medicalprofile.heartattack,
            "CHF": self.user.medicalprofile.CHF,
            "stroke": self.user.medicalprofile.stroke,
            "PVD": self.user.medicalprofile.PVD,
            "treatment": Advil,
        }

    def test_form_valid(self):
        form = FlareForm(data=self.flare_data)
        urate_form = UrateFlareForm(data=self.urate_data)
        form.instance.user = self.user
        urate_form.instance.user = self.user
        self.assertTrue(form.is_valid())
        self.assertTrue(urate_form.is_valid())
        # Test that user can be assigned to form instance
        self.assertEqual(form.instance.user, self.user)
        self.assertEqual(urate_form.instance.user, self.user)

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

    def test_post(self):
        self.client.force_login(self.user)
        self.flare_data.urate = self.urate_data
        response = self.client.post(reverse("flare:create"), self.flare_data)
        flare = Flare.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Flare.objects.count(), 1)
        self.assertEqual(flare.user, self.user)
        self.assertEqual(flare.monoarticular, self.flare_data.get("monoarticular"))
        self.assertEqual(flare.male, self.flare_data.get("male"))
        self.assertEqual(flare.prior_gout, self.flare_data.get("prior_gout"))
        self.assertEqual(flare.onset, self.flare_data.get("onset"))
        self.assertEqual(flare.redness, self.flare_data.get("redness"))
        self.assertEqual(self.flare_data.get("firstmtp"), flare.firstmtp)
        # self.assertIn(self.flare_data.get("location"), flare.location)
        self.assertEqual(flare.hypertension, self.user.medicalprofile.hypertension)
        self.assertEqual(flare.heartattack, self.user.medicalprofile.heartattack)
        self.assertEqual(flare.CHF, self.user.medicalprofile.CHF)
        self.assertEqual(flare.stroke, self.user.medicalprofile.stroke)
        self.assertEqual(flare.stroke, self.user.medicalprofile.stroke)
        self.assertEqual(flare.urate, self.flare_data.get("urate"))
