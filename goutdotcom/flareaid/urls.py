from django.urls import path

from .views import FlareAidCreate, FlareAidDetail, FlareAidList, FlareAidUpdate

app_name = "flareaid"
urlpatterns = [
    path("<int:pk>/", view=FlareAidDetail.as_view(), name="detail"),
    path("<int:pk>/update/", view=FlareAidUpdate.as_view(), name="update"),
    path("<int:pk>/update/flare/<int:flare>/", view=FlareAidUpdate.as_view(), name="flare-update"),
    path("create/", view=FlareAidCreate.as_view(), name="create"),
    path("create/flare/<int:flare>/", view=FlareAidCreate.as_view(), name="flareaid-create"),
    path("", view=FlareAidList.as_view(), name="list"),
]
