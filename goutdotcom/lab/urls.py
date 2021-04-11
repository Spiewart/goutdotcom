from django.urls import path

from .views import (
    UrateCreate,
    UrateDetail,
    UrateList,
)

app_name = "lab"
urlpatterns = [
    path("urate/", view=UrateList.as_view(), name="urate-list"),
    path("urate/create/", view=UrateCreate.as_view(), name="create"),
    path("urate/<int:pk>/", view=UrateDetail.as_view(), name="urate-detail"),
]
