from django.test import RequestFactory, TestCase
from django.urls import reverse

from ...profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)

from ...ult.tests.factories import ULTFactory
from ...users.tests.factories import UserFactory
from ..forms import ULTAidForm
from ..models import ULTAid
from ..tests.factories import ULTAidFactory
from ..views import ULTAidCreate, ULTAidUpdate


class TestCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(username="bumblyboy")
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ult = ULTFactory(user=self.user)
        self.ultaid_data = {
            "user": self.user,
            "need": True,
            "want": True,
            "ckd": self.user.medicalprofile.CKD,
            "XOI_interactions": self.user.medicalprofile.XOI_interactions,
            "organ_transplant": self.user.medicalprofile.organ_transplant,
            "allopurinol_hypersensitivity": self.user.medicalprofile.allopurinol_hypersensitivity,
            "febuxostat_hypersensitivity": self.user.medicalprofile.febuxostat_hypersensitivity,
            "heartattack": self.user.medicalprofile.heartattack,
            "stroke": self.user.medicalprofile.stroke,
        }

        self.ultaid_data_no_user = {
            "need": True,
            "want": True,
            "ckd": self.user.medicalprofile.CKD,
            "XOI_interactions": self.user.medicalprofile.XOI_interactions,
            "organ_transplant": self.user.medicalprofile.organ_transplant,
            "allopurinol_hypersensitivity": self.user.medicalprofile.allopurinol_hypersensitivity,
            "febuxostat_hypersensitivity": self.user.medicalprofile.febuxostat_hypersensitivity,
            "heartattack": self.user.medicalprofile.heartattack,
            "stroke": self.user.medicalprofile.stroke,
        }

        self.user2 = UserFactory(username="bumblyboy2")
        self.patientprofile2 = PatientProfileFactory(user=self.user2)
        self.medicalprofile2 = MedicalProfileFactory(user=self.user2)
        self.familyprofile2 = FamilyProfileFactory(user=self.user2)
        self.socialprofile2 = SocialProfileFactory(user=self.user2)
        self.ultaid2 = ULTAidFactory(
            user=self.user2,
            ckd=self.user2.medicalprofile.CKD,
            XOI_interactions=self.user2.medicalprofile.XOI_interactions,
            organ_transplant=self.user2.medicalprofile.organ_transplant,
            allopurinol_hypersensitivity=self.user2.medicalprofile.allopurinol_hypersensitivity,
            febuxostat_hypersensitivity=self.user2.medicalprofile.febuxostat_hypersensitivity,
            heartattack=self.user2.medicalprofile.heartattack,
            stroke=self.user2.medicalprofile.stroke,
        )

    def test_form_valid(self):
        form = ULTAidForm(data=self.ultaid_data)
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        # Test that user can be assigned to form instance
        self.assertEqual(form.instance.user, self.user)

    def test_get_context_data(self):
        request = self.factory.get("/ultaid/create")
        request.user = self.user
        response = ULTAidCreate.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn("CKD_form", response.context_data)
        self.assertIn("XOI_interactions_form", response.context_data)
        self.assertIn("organ_transplant_form", response.context_data)
        self.assertIn("allopurinol_hypersensitivity_form", response.context_data)
        self.assertIn("febuxostat_hypersensitivity_form", response.context_data)
        self.assertIn("heartattack_form", response.context_data)
        self.assertIn("stroke_form", response.context_data)

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("ultaid:create"), self.ultaid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ultaid/ultaid_form.html")
        ### NEED TO FIGURE OUT HOW TO TEST FETCH OF EXISTING ULT
        # Checks if ult:create redirects for user2 who already has a ULT that exists
        self.client.force_login(self.user2)
        response2 = self.client.get(reverse("ultaid:create"))
        self.assertEqual(response2.status_code, 302)

    def test_get_success_url(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("ultaid:create"), self.ultaid_data)
        ultaid = ULTAid.objects.last()
        self.assertRedirects(response, reverse("ultaid:detail", kwargs={"pk": ultaid.pk}))

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("ultaid:create"), self.ultaid_data)
        ultaid = ULTAid.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ULTAid.objects.count(), 2)
        self.assertEqual(ultaid.need, self.ultaid_data.get("need"))
        self.assertEqual(ultaid.want, self.ultaid_data.get("want"))
        self.assertEqual(ultaid.user, self.user)
        self.assertEqual(ultaid.ckd, self.user.medicalprofile.CKD)
        self.assertEqual(ultaid.XOI_interactions, self.user.medicalprofile.XOI_interactions)
        self.assertEqual(ultaid.organ_transplant, self.user.medicalprofile.organ_transplant)
        self.assertEqual(ultaid.allopurinol_hypersensitivity, self.user.medicalprofile.allopurinol_hypersensitivity)
        self.assertEqual(ultaid.febuxostat_hypersensitivity, self.user.medicalprofile.febuxostat_hypersensitivity)
        self.assertEqual(ultaid.heartattack, self.user.medicalprofile.heartattack)
        self.assertEqual(ultaid.stroke, self.user.medicalprofile.stroke)


class TestUpdateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(username="bumblyboy")
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ultaid = ULTAidFactory(user=self.user)
        # Create user-associated ULT for use by ULTAid view, which adds it to the context for JQuery form field updates
        self.ult = ULTFactory(user=self.user)
        self.ultaid_data = {
            "user": self.user,
            "need": True,
            "want": True,
            "ckd": self.user.medicalprofile.CKD,
            "XOI_interactions": self.user.medicalprofile.XOI_interactions,
            "organ_transplant": self.user.medicalprofile.organ_transplant,
            "allopurinol_hypersensitivity": self.user.medicalprofile.allopurinol_hypersensitivity,
            "febuxostat_hypersensitivity": self.user.medicalprofile.febuxostat_hypersensitivity,
            "heartattack": self.user.medicalprofile.heartattack,
            "stroke": self.user.medicalprofile.stroke,
        }
        self.update_url = reverse("ultaid:update", kwargs={"pk": self.ultaid.pk})

    def test_get_context_data(self):
        request = self.factory.get(self.update_url)
        request.user = self.user
        response = ULTAidUpdate.as_view()(request, pk=self.ultaid.pk)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn("CKD_form", response.context_data)
        self.assertIn("XOI_interactions_form", response.context_data)
        self.assertIn("organ_transplant_form", response.context_data)
        self.assertIn("allopurinol_hypersensitivity_form", response.context_data)
        self.assertIn("febuxostat_hypersensitivity_form", response.context_data)
        self.assertIn("heartattack_form", response.context_data)
        self.assertIn("stroke_form", response.context_data)

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("ultaid:update", kwargs={"pk": self.ultaid.pk}), self.ultaid_data)
        ultaid = ULTAid.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ULTAid.objects.count(), 1)
        self.assertEqual(ultaid.need, self.ultaid_data.get("need"))
        self.assertEqual(ultaid.want, self.ultaid_data.get("want"))
        self.assertEqual(ultaid.user, self.user)
        self.assertEqual(ultaid.ckd, self.user.medicalprofile.CKD)
        self.assertEqual(ultaid.XOI_interactions, self.user.medicalprofile.XOI_interactions)
        self.assertEqual(ultaid.organ_transplant, self.user.medicalprofile.organ_transplant)
        self.assertEqual(ultaid.allopurinol_hypersensitivity, self.user.medicalprofile.allopurinol_hypersensitivity)
        self.assertEqual(ultaid.febuxostat_hypersensitivity, self.user.medicalprofile.febuxostat_hypersensitivity)
        self.assertEqual(ultaid.heartattack, self.user.medicalprofile.heartattack)
        self.assertEqual(ultaid.stroke, self.user.medicalprofile.stroke)
