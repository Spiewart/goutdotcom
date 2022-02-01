from django.urls import path

from goutdotcom.users.views import (
    provider_patient_list_view,
    user_create_view,
    user_detail_view,
    user_provider_detail_view,
    user_provider_update_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("create/", view=user_create_view, name="create"),
    path("provider/<str:username>/patients/", view=provider_patient_list_view, name="provider-patient-list"),
    path("update/<str:username>/", view=user_provider_update_view, name="provider-update"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<int:pk>/", view=user_provider_detail_view, name="provider-user-detail"),
]
