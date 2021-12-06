from django.test import RequestFactory, TestCase
from django.urls import reverse

from ...profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)
from ...users.tests.factories import UserFactory
from ..forms import FlareAidForm
from ..models import FlareAid
from ..tests.factories import FlareAidFactory
from ..views import FlareAidCreate, FlareAidList, FlareAidUpdate


class TestCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(username="bumblyboy")
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.flareaid_data = {
            "user": self.user,
            "perfect_health": True,
            "monoarticular": True,
            "anticoagulation": self.user.medicalprofile.anticoagulation,
            "bleed": self.user.medicalprofile.bleed,
            "ckd": self.user.medicalprofile.CKD,
            "colchicine_interactions": self.user.medicalprofile.colchicine_interactions,
            "diabetes": self.user.medicalprofile.diabetes,
            "heartattack": self.user.medicalprofile.heartattack,
            "ibd": self.user.medicalprofile.IBD,
            "osteoporosis": self.user.medicalprofile.osteoporosis,
            "stroke": self.user.medicalprofile.stroke,
        }

    def test_form_valid(self):
        form = FlareAidForm(data=self.flareaid_data)
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        # Test that user can be assigned to form instance
        self.assertEqual(form.instance.user, self.user)

    def test_get_context_data(self):
        request = self.factory.get("/flareaid/create")
        request.user = self.user
        response = FlareAidCreate.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn("anticoagulation_form", response.context_data)
        self.assertIn("bleed_form", response.context_data)
        self.assertIn("CKD_form", response.context_data)
        self.assertIn("colchicine_interactions_form", response.context_data)
        self.assertIn("diabetes_form", response.context_data)
        self.assertIn("heartattack_form", response.context_data)
        self.assertIn("IBD_form", response.context_data)
        self.assertIn("osteoporosis_form", response.context_data)
        self.assertIn("stroke_form", response.context_data)

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("flareaid:create"), self.flareaid_data)
        flareaid = FlareAid.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FlareAid.objects.count(), 1)
        self.assertEqual(flareaid.perfect_health, self.flareaid_data.get("perfect_health"))
        self.assertEqual(flareaid.monoarticular, self.flareaid_data.get("monoarticular"))
        self.assertEqual(flareaid.user, self.user)
        self.assertEqual(flareaid.anticoagulation, self.user.medicalprofile.anticoagulation)
        self.assertEqual(flareaid.bleed, self.user.medicalprofile.bleed)
        self.assertEqual(flareaid.ckd, self.user.medicalprofile.CKD)
        self.assertEqual(flareaid.colchicine_interactions, self.user.medicalprofile.colchicine_interactions)
        self.assertEqual(flareaid.diabetes, self.user.medicalprofile.diabetes)
        self.assertEqual(flareaid.heartattack, self.user.medicalprofile.heartattack)
        self.assertEqual(flareaid.ibd, self.user.medicalprofile.IBD)
        self.assertEqual(flareaid.osteoporosis, self.user.medicalprofile.osteoporosis)
        self.assertEqual(flareaid.stroke, self.user.medicalprofile.stroke)

class TestUpdateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(username="bumblyboy")
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.flareaid = FlareAidFactory(user=self.user)
        self.flareaid_data = {
            "user": self.user,
            "perfect_health": True,
            "monoarticular": True,
            "anticoagulation": self.user.medicalprofile.anticoagulation,
            "bleed": self.user.medicalprofile.bleed,
            "ckd": self.user.medicalprofile.CKD,
            "colchicine_interactions": self.user.medicalprofile.colchicine_interactions,
            "diabetes": self.user.medicalprofile.diabetes,
            "heartattack": self.user.medicalprofile.heartattack,
            "ibd": self.user.medicalprofile.IBD,
            "osteoporosis": self.user.medicalprofile.osteoporosis,
            "stroke": self.user.medicalprofile.stroke,
        }
        self.update_url = reverse("flareaid:update", kwargs={"pk": self.flareaid.pk})

    def test_get_context_data(self):
        request = self.factory.get(self.update_url)
        request.user = self.user
        response = FlareAidUpdate.as_view()(request, pk=self.flareaid.pk)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn("anticoagulation_form", response.context_data)
        self.assertIn("bleed_form", response.context_data)
        self.assertIn("CKD_form", response.context_data)
        self.assertIn("colchicine_interactions_form", response.context_data)
        self.assertIn("diabetes_form", response.context_data)
        self.assertIn("heartattack_form", response.context_data)
        self.assertIn("IBD_form", response.context_data)
        self.assertIn("osteoporosis_form", response.context_data)
        self.assertIn("stroke_form", response.context_data)

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("flareaid:update", kwargs={"pk": self.flareaid.pk}), self.flareaid_data)
        flareaid = FlareAid.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FlareAid.objects.count(), 1)
        self.assertEqual(flareaid.perfect_health, self.flareaid_data.get("perfect_health"))
        self.assertEqual(flareaid.monoarticular, self.flareaid_data.get("monoarticular"))
        self.assertEqual(flareaid.user, self.user)
        self.assertEqual(flareaid.anticoagulation, self.user.medicalprofile.anticoagulation)
        self.assertEqual(flareaid.bleed, self.user.medicalprofile.bleed)
        self.assertEqual(flareaid.ckd, self.user.medicalprofile.CKD)
        self.assertEqual(flareaid.colchicine_interactions, self.user.medicalprofile.colchicine_interactions)
        self.assertEqual(flareaid.diabetes, self.user.medicalprofile.diabetes)
        self.assertEqual(flareaid.heartattack, self.user.medicalprofile.heartattack)
        self.assertEqual(flareaid.ibd, self.user.medicalprofile.IBD)
        self.assertEqual(flareaid.osteoporosis, self.user.medicalprofile.osteoporosis)
        self.assertEqual(flareaid.stroke, self.user.medicalprofile.stroke)
