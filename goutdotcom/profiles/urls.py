from django.urls import path

from .views import (
    ContraindicationsProfileCreate,
    ContraindicationsProfileUpdate,
    MedicalProfileCreate,
    MedicalProfileUpdate,
    PatientProfileCreate,
    PatientProfileUpdate,
)

app_name = "profiles"
urlpatterns = [
    path("create/", view=PatientProfileCreate.as_view(), name="create"),
    path("create/contraindications/", view=ContraindicationsProfileCreate.as_view(), name="create-contraindications"),
    path("create/medical/", view=MedicalProfileCreate.as_view(), name="create-medical"),
    path("<user>/contraindications/<int:pk>/update/", view=ContraindicationsProfileUpdate.as_view(), name="update-contraindications"),
    path("<user>/medical/<int:pk>/update/", view=MedicalProfileUpdate.as_view(), name="update-medical"),
    path("<user>/<int:pk>/update/", view=PatientProfileUpdate.as_view(), name="update"),
]
