from django.urls import path

from profiles.views import (
    PatientProfileUpdate,
)

app_name = "profiles"
urlpatterns = [
    path("<str:username>/<pk:pk>/update", view=PatientProfileUpdate, name="update"),
]
