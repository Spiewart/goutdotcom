from django.urls import path

from .views import FlareAidCreate, FlareAidDetail, FlareAidList, FlareAidUpdate

app_name = "flareaid"
urlpatterns = [
    path("<int:pk>/", view=FlareAidDetail.as_view(), name="detail"),
    path("<int:pk>/update/", view=FlareAidUpdate.as_view(), name="update"),
    path("create/", view=FlareAidCreate.as_view(), name="create"),
    path("", view=FlareAidList.as_view(), name="list"),
]
