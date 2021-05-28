from django.urls import path
from django.views.generic import TemplateView

from . import views

from .views import (
    FlareCreate,
    FlareDetail,
    FlareUpdate,
    FlareList,
    IndexView,
)

app_name = "flare"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("landing/", TemplateView.as_view(template_name="flare/landing.html"), name="landing"),
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("create/", view=FlareCreate.as_view(), name="create"),
    path("<int:id>/flareurateupdate/", views.FlareUrateUpdate, name="flareurateupdate"),
    path("<int:pk>/update/", view=FlareUpdate.as_view(), name="update"),
    path("flareuratecreate/", views.FlareUrateCreate, name="flareuratecreate"),
    path("flaremeduratecreate/", views.FlareMedUrateCreate, name="flaremeduratecreate"),
    path("list", view=FlareList.as_view(), name="list"),
]
