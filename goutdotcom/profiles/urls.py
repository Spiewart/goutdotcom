from django.urls import path

from .views import (
    PatientProfileCreate,
    PatientProfileUpdate,
)

app_name = "profiles"
urlpatterns = [
    path("create/", view=PatientProfileCreate.as_view(), name="create"),
    path("<user>/<int:pk>/update/", view=PatientProfileUpdate.as_view(), name="update"),
]
