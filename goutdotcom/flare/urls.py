from django.urls import path
from django.views.generic import TemplateView

from . import views

from .views import (
    FlareCreate,
    FlareDetail,
    FlareUpdate,
    FlareList,
)

app_name = "flare"
urlpatterns = [
    path("", TemplateView.as_view(template_name="flare/index.html"), name="index"),
    path("landing/", TemplateView.as_view(template_name="flare/landing.html"), name="landing"),
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("create/", view=FlareCreate.as_view(), name="create"),
    path("<int:pk>/update/", view=FlareUpdate.as_view(), name="update"),
    path("flareuratecreate/", views.FlareUrateCreate, name="flareuratecreate"),
    path("list", view=FlareList.as_view(), name="list"),
]
