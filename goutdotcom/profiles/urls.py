from django.urls import path

from .views import (
    PatientProfileUpdate,
)

app_name = "profiles"
urlpatterns = [
    path("<slug:slug>/update", view=PatientProfileUpdate.as_view(), name="update"),
]
