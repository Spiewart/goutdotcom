from decimal import *

from django.forms.models import model_to_dict
from django.test import RequestFactory, TestCase
from django.urls import reverse

from goutdotcom.history.tests.factories import (
    AnginaFactory,
    CHFFactory,
    HeartAttackFactory,
    HypertensionFactory,
    PVDFactory,
    StrokeFactory,
)

from ...lab.forms import UrateFlareForm
from ...lab.models import Urate
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
        self.urate = UrateFactory()
        self.flare_data = {
            "monoarticular": True,
            "male": True,
            "prior_gout": True,
            "onset": True,
            "redness": True,
            "firstmtp": True,
            "angina": AnginaFactory(),
            "hypertension": HypertensionFactory(),
            "heartattack": HeartAttackFactory(),
            "CHF": CHFFactory(),
            "stroke": StrokeFactory(),
            "PVD": PVDFactory(),
        }

        self.flare_data_user = {
            "user": self.user,
            "monoarticular": True,
            "male": True,
            "prior_gout": True,
            "onset": True,
            "redness": True,
            "firstmtp": True,
            "angina": self.user.medicalprofile.angina,
            "hypertension": self.user.medicalprofile.hypertension,
            "heartattack": self.user.medicalprofile.heartattack,
            "CHF": self.user.medicalprofile.CHF,
            "stroke": self.user.medicalprofile.stroke,
            "PVD": self.user.medicalprofile.PVD,
        }

        self.flare_data_urate = {
            "user": self.user,
            "monoarticular": True,
            "male": True,
            "prior_gout": True,
            "onset": True,
            "redness": True,
            "firstmtp": True,
            "angina": self.user.medicalprofile.angina,
            "hypertension": self.user.medicalprofile.hypertension,
            "heartattack": self.user.medicalprofile.heartattack,
            "CHF": self.user.medicalprofile.CHF,
            "stroke": self.user.medicalprofile.stroke,
            "PVD": self.user.medicalprofile.PVD,
            "urate": Urate.objects.get(pk=self.urate.pk),
        }

    def test_form_valid(self):
        form = FlareForm(data=self.flare_data)
        self.assertTrue(form.is_valid())
        self.flare_data["location"] = ["Right foot"]
        form = FlareForm(data=self.flare_data)
        self.assertTrue(form.is_valid())
        self.flare_data["urate"] = UrateFactory()
        form = FlareForm(data=self.flare_data)
        self.assertTrue(form.is_valid())
        # Test that user can be assigned to form instance
        form_user = FlareForm(data=self.flare_data_user)
        self.assertTrue(form_user.is_valid())
        self.assertEqual(form_user.instance.user, self.user)

    def test_get_context_data(self):
        request = self.factory.get("/flare/create")
        request.user = self.user
        response = FlareCreate.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn("angina_form", response.context_data)
        self.assertIn("hypertension_form", response.context_data)
        self.assertIn("heartattack_form", response.context_data)
        self.assertIn("CHF_form", response.context_data)
        self.assertIn("stroke_form", response.context_data)
        self.assertIn("PVD_form", response.context_data)

    def test_post_no_urate(self):
        self.client.force_login(self.user)
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
        response = self.client.post(reverse("flare:create"), self.flare_data, urate=self.urate)
        flare = Flare.objects.last()
        self.assertEqual(flare.urate, self.flare_data_urate.get("urate"))
