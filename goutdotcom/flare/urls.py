from django.urls import path

from .views import (
    AboutFlares,
    FlareCreate,
    FlareDetail,
    FlareUpdate,
    FlareList,
)

app_name = "flare"
urlpatterns = [
    path("about/", view=AboutFlares.as_view(), name="about"),
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("<int:pk>/update/", view=FlareUpdate.as_view(), name="update"),
    path("create/", view=FlareCreate.as_view(), name="create"),
    path("", view=FlareList.as_view(), name="list"),
]
