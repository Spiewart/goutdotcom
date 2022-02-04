from django.urls import path

from .views import (
    FamilyProfileUpdate,
    MedicalProfileUpdate,
    PatientProfileUpdate,
    ProviderProfileUpdate,
    SocialProfileUpdate,
)

app_name = "profiles"
urlpatterns = [
    path("<slug:slug>/family/update/", view=FamilyProfileUpdate.as_view(), name="update-family"),
    path("<slug:slug>/medical/update/", view=MedicalProfileUpdate.as_view(), name="update-medical"),
    path("<slug:slug>/social/update/", view=SocialProfileUpdate.as_view(), name="update-social"),
    path("<slug:slug>/update/", view=PatientProfileUpdate.as_view(), name="update"),
    path("provider/<slug:slug>/update/", view=ProviderProfileUpdate.as_view(), name="provider-update"),
]
