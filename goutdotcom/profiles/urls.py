from django.urls import path

from .views import (
    FamilyProfileCreate,
    FamilyProfileUpdate,
    MedicalProfileCreate,
    MedicalProfileUpdate,
    PatientProfileCreate,
    PatientProfileUpdate,
    ProviderProfileUpdate,
    SocialProfileCreate,
    SocialProfileUpdate,
)

app_name = "profiles"
urlpatterns = [
    path("create/", view=PatientProfileCreate.as_view(), name="create"),
    path("create/family/", view=FamilyProfileCreate.as_view(), name="create-family"),
    path("create/medical/", view=MedicalProfileCreate.as_view(), name="create-medical"),
    path("create/social/", view=SocialProfileCreate.as_view(), name="create-social"),
    path("<user>/family/<int:pk>/update/", view=FamilyProfileUpdate.as_view(), name="update-family"),
    path("<user>/medical/<int:pk>/update/", view=MedicalProfileUpdate.as_view(), name="update-medical"),
    path("<user>/social/<int:pk>/update/", view=SocialProfileUpdate.as_view(), name="update-social"),
    path("<user>/<int:pk>/update/", view=PatientProfileUpdate.as_view(), name="update"),
    path("provider/<user>/<int:pk>/update/", view=ProviderProfileUpdate.as_view(), name="provider-update"),
]
