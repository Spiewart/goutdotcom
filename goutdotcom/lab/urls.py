from django.urls import path

from .views import (
    IndexView,
    LabAbout,
    LabCreate,
    LabDetail,
    LabList,
    LabUpdate,
)

app_name = "lab"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("about/<lab>/", view=LabAbout.as_view(), name="about"),
    path("create/<lab>/", view=LabCreate.as_view(), name="create"),
    path("list/<lab>/", view=LabList.as_view(), name="list"),
    path("update/<lab>/<int:pk>/", view=LabUpdate.as_view(), name="update"),
    path("<lab>/<int:pk>/", view=LabDetail.as_view(), name="detail"),
]
