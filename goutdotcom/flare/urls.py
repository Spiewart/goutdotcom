from django.urls import path
from django.views.generic import TemplateView

from .views import (
    FlareDetail,
    FlareCreate,
    FlareUpdate,
)

app_name = "flare"
urlpatterns = [
    path("", TemplateView.as_view(template_name="flare/index.html"), name="index"),
    path("create/", view=FlareCreate.as_view(), name="create"),
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("<int:pk>/update/", view=FlareUpdate.as_view(), name="update"),
]
