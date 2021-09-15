from django.urls import path

from .views import MedicalProfileCreate, PatientProfileCreate, PatientProfileUpdate

app_name = "profiles"
urlpatterns = [
    path("create/", view=PatientProfileCreate.as_view(), name="create"),
    path("create/medical/", view=MedicalProfileCreate.as_view(), name="create-medical"),
    path("<user>/<int:pk>/update/", view=PatientProfileUpdate.as_view(), name="update"),
]
