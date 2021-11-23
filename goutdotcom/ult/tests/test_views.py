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
from ..tests.factories import ULTFactory
from ..views import ULTCreate, ULTDetail, ULTUpdate


class TestCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.patientprofile = PatientProfileFactory(user=self.user)
        self.medicalprofile = MedicalProfileFactory(user=self.user)
        self.familyprofile = FamilyProfileFactory(user=self.user)
        self.socialprofile = SocialProfileFactory(user=self.user)
        self.ult_data = {
            "user": self.user,
            "num_flares": "one",
            "freq_flares": "two or more",
            "erosions": self.medicalprofile.erosions,
            "tophi": self.medicalprofile.tophi,
            "ckd": self.medicalprofile.CKD,
            "stones": self.medicalprofile.urate_kidney_stones,
            "hyperuricemia": self.medicalprofile.hyperuricemia,
        }

    def test_form_valid(self):
        form = ULTForm(data=self.ult_data)
        self.assertTrue(form.is_valid())

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
