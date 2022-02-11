from django.urls import path

from .views import AboutFlares, FlareCreate, FlareDetail, FlareList, FlareUpdate

app_name = "flare"
urlpatterns = [
    path("about/", view=AboutFlares.as_view(), name="about"),
    path("create/", view=FlareCreate.as_view(), name="create"),
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("<slug:slug>/", view=FlareDetail.as_view(), name="user-detail"),
    path("<slug:username>/create/", view=FlareCreate.as_view(), name="user-create"),
    path("<slug:slug>/update/", view=FlareUpdate.as_view(), name="update"),
    path("list/<slug:username>/", view=FlareList.as_view(), name="list"),
]
