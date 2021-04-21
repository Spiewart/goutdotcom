from django.urls import path

from .views import (
    PatientProfileCreate,
    PatientProfileUpdate,
)

app_name = "profiles"
urlpatterns = [
    path("create/", view=PatientProfileCreate.as_view(), name="create"),
    path("<slug:slug>/update", view=PatientProfileUpdate.as_view(), name="update"),
]
