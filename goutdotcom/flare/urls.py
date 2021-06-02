from django.urls import path
from django.views.generic import TemplateView

from . import views

from .views import (
    FlareDetail,
    FlareUpdate,
    FlareList,
    IndexView,
)

app_name = "flare"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("<int:id>/flareurateupdate/", views.FlareUrateUpdate, name="flareurateupdate"),
    path("<int:pk>/update/", view=FlareUpdate.as_view(), name="update"),
    path("create/", views.FlareCreate, name="flarecreate"),
    path("list", view=FlareList.as_view(), name="list"),
]
