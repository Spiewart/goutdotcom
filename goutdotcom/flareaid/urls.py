from django.urls import path

from .views import FlareAidCreate, FlareAidDetail, FlareAidList, FlareAidUpdate

app_name = "flareaid"
urlpatterns = [
    path("<int:pk>/", view=FlareAidDetail.as_view(), name="detail"),
    path("<slug:slug>/update/", view=FlareAidUpdate.as_view(), name="update"),
    path("<slug:slug>/update/flare/<slug:flare>/", view=FlareAidUpdate.as_view(), name="flare-update"),
    path("create/", view=FlareAidCreate.as_view(), name="create"),
    path("<slug:slug>/", view=FlareAidDetail.as_view(), name="user-detail"),
    path("<slug:username>/create/", view=FlareAidCreate.as_view(), name="user-create"),
    path("create/flare/<int:flare>/", view=FlareAidCreate.as_view(), name="flare-create"),
    path("<slug:username>/create/flare/<int:flare>/", view=FlareAidCreate.as_view(), name="user-flare-create"),
    path("list/<slug:username>/", view=FlareAidList.as_view(), name="list"),
]
