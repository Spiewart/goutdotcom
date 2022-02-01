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
    path("family/<int:pk>/update/", view=FamilyProfileUpdate.as_view(), name="provider-update-family"),
    path("medical/<int:pk>/update/", view=MedicalProfileUpdate.as_view(), name="provider-update-medical"),
    path("social/<int:pk>/update/", view=SocialProfileUpdate.as_view(), name="provider-update-social"),
    path("<int:pk>/update/", view=PatientProfileUpdate.as_view(), name="provider-update"),
    path("<user>/family/<int:pk>/update/", view=FamilyProfileUpdate.as_view(), name="update-family"),
    path("<user>/medical/<int:pk>/update/", view=MedicalProfileUpdate.as_view(), name="update-medical"),
    path("<user>/social/<int:pk>/update/", view=SocialProfileUpdate.as_view(), name="update-social"),
    path("<user>/<int:pk>/update/", view=PatientProfileUpdate.as_view(), name="update"),
    path("provider/<user>/<int:pk>/update/", view=ProviderProfileUpdate.as_view(), name="provider-update"),
]
