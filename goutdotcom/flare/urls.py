from django.urls import path
from django.views.generic import TemplateView, FormView

from . import views

from .views import (
    FlareDetail,
    FlareUpdate,
    FlareList,
)

app_name = "flare"
urlpatterns = [
    path("", TemplateView.as_view(template_name="flare/index.html"), name="index"),
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("<int:pk>/update/", view=FlareUpdate.as_view(), name="update"),
    path("create/", views.FlareCreate, name="create"),
    path("list", view=FlareList.as_view(), name="list"),
]
