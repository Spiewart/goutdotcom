from django.urls import path
from django.views.generic import TemplateView, FormView

from . import views

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
    path("flareuratecreate/", views.FlareUrateCreate, name="flare-urate-create"),
    path("flare2create/", views.Flare2Create, name="flare2create"),
]
