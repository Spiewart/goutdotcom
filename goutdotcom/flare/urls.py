from django.urls import path
from django.views.generic import TemplateView

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
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("<int:pk>/update/", view=FlareUpdate.as_view(), name="update"),
    path("create/", view=FlareCreate.as_view(), name="create"),
    path("list", view=FlareList.as_view(), name="list"),
]
