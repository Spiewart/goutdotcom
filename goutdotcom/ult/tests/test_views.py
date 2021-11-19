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

    def test_get_sucess_url(self):
        request = self.factory.post(ULTCreate, data=self.ult_data)
        request.data = {"id": 1}
        request.user = self.user
        response = ULTCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("ult:detail", kwargs={"pk": 1}), fetch_redirect_response=False)
