from django.urls import path

from .views import (
    PatientProfileUpdate,
)

app_name = "profiles"
urlpatterns = [
    path("<int:pk>/update", view=PatientProfileUpdate, name="update"),
]
