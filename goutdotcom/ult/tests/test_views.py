from django.apps import apps
from django.test import RequestFactory, TestCase
from django.urls import reverse

from goutdotcom.profiles.tests.factories import (
    FamilyProfileFactory,
    MedicalProfileFactory,
    PatientProfileFactory,
    SocialProfileFactory,
)

from ...history.tests.factories import (
    CKDFactory,
    ErosionsFactory,
    HyperuricemiaFactory,
    TophiFactory,
    UrateKidneyStonesFactory,
)
from ...users.tests.factories import UserFactory
from ..forms import ULTForm
from ..models import ULT
from ..tests.factories import ULTFactory
from ..views import ULTCreate, ULTDetail, ULTUpdate


class TestCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(username="bumblyboy")
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ult_data = {
            "user": self.user,
            "num_flares": "one",
            "freq_flares": "two or more",
            "erosions": self.user.medicalprofile.erosions,
            "tophi": self.user.medicalprofile.tophi,
            "stones": self.user.medicalprofile.urate_kidney_stones,
            "ckd": self.user.medicalprofile.CKD,
            "hyperuricemia": self.user.medicalprofile.hyperuricemia,
        }

        self.ult_data_no_user = {
            "num_flares": "one",
            "freq_flares": "two or more",
            "erosions": self.user.medicalprofile.erosions,
            "tophi": self.user.medicalprofile.tophi,
            "stones": self.user.medicalprofile.urate_kidney_stones,
            "ckd": self.user.medicalprofile.CKD,
            "hyperuricemia": self.user.medicalprofile.hyperuricemia,
        }

        self.user2 = UserFactory(username="bumblyboy2")
        self.patientprofile2 = PatientProfileFactory(user=self.user2)
        self.medicalprofile2 = MedicalProfileFactory(user=self.user2)
        self.familyprofile2 = FamilyProfileFactory(user=self.user2)
        self.socialprofile2 = SocialProfileFactory(user=self.user2)
        self.ult2 = ULTFactory(
            user=self.user2,
            ckd=self.user2.medicalprofile.CKD,
            erosions=self.user2.medicalprofile.erosions,
            tophi=self.user2.medicalprofile.tophi,
            stones=self.user2.medicalprofile.urate_kidney_stones,
            hyperuricemia=self.user2.medicalprofile.hyperuricemia,
        )

    def test_form_valid(self):
        form = ULTForm(data=self.ult_data)
        self.assertTrue(form.is_valid())
        form_no_user = ULTForm(data=self.ult_data_no_user)
        self.assertTrue(form_no_user.is_valid())

    def test_get_context_data(self):
        request = self.factory.get("/ult/create")
        request.user = self.user
        response = ULTCreate.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn("CKD_form", response.context_data)
        self.assertIn("erosions_form", response.context_data)
        self.assertIn("hyperuricemia_form", response.context_data)
        self.assertIn("tophi_form", response.context_data)
        self.assertIn("urate_kidney_stones_form", response.context_data)

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("ult:create"), self.ult_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ult/ult_form.html")
        ### NEED TO FIGURE OUT HOW TO TEST FETCH OF EXISTING ULT
        # Checks if ult:create redirects for user2 who already has a ULT that exists
        self.client.force_login(self.user2)
        response2 = self.client.get(reverse("ult:create"))
        self.assertEqual(response2.status_code, 302)

    def test_get_success_url(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("ult:create"), self.ult_data)
        ult = ULT.objects.last()
        self.assertRedirects(response, reverse("ult:detail", kwargs={"pk": ult.pk}))

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("ult:create"), self.ult_data)
        ult = ULT.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ULT.objects.count(), 2)
        self.assertEqual(ult.num_flares, self.ult_data.get("num_flares"))
        self.assertEqual(ult.freq_flares, self.ult_data.get("freq_flares"))
        self.assertEqual(ult.user, self.user)
        self.assertEqual(ult.ckd, self.user.medicalprofile.CKD)
        self.assertEqual(ult.erosions, self.user.medicalprofile.erosions)
        self.assertEqual(ult.tophi, self.user.medicalprofile.tophi)
        self.assertEqual(ult.hyperuricemia, self.user.medicalprofile.hyperuricemia)
        self.assertEqual(ult.stones, self.user.medicalprofile.urate_kidney_stones)


class TestUpdateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(username="bumblyboy")
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ult = ULTFactory(user=self.user)
        self.ult_data = {
            "user": self.user,
            "num_flares": "one",
            "freq_flares": "two or more",
            "erosions": self.user.medicalprofile.erosions,
            "tophi": self.user.medicalprofile.tophi,
            "stones": self.user.medicalprofile.urate_kidney_stones,
            "ckd": self.user.medicalprofile.CKD,
            "hyperuricemia": self.user.medicalprofile.hyperuricemia,
        }
        self.update_url = reverse("ult:update", kwargs={"pk": self.ult.pk})

    def test_get_context_data(self):
        request = self.factory.get(self.update_url)
        request.user = self.user
        response = ULTUpdate.as_view()(request, pk=self.ult.pk)
        self.assertIsInstance(response.context_data, dict)
        self.assertIn("CKD_form", response.context_data)
        self.assertIn("erosions_form", response.context_data)
        self.assertIn("hyperuricemia_form", response.context_data)
        self.assertIn("tophi_form", response.context_data)
        self.assertIn("urate_kidney_stones_form", response.context_data)

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("ult:update", kwargs={"pk": self.ult.pk}), self.ult_data)
        ult = ULT.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ULT.objects.count(), 1)
        self.assertEqual(ult.num_flares, self.ult_data.get("num_flares"))
        self.assertEqual(ult.freq_flares, self.ult_data.get("freq_flares"))
        self.assertEqual(ult.user, self.user)
        self.assertEqual(ult.ckd, self.user.medicalprofile.CKD)
        self.assertEqual(ult.erosions, self.user.medicalprofile.erosions)
        self.assertEqual(ult.tophi, self.user.medicalprofile.tophi)
        self.assertEqual(ult.hyperuricemia, self.user.medicalprofile.hyperuricemia)
        self.assertEqual(ult.stones, self.user.medicalprofile.urate_kidney_stones)
