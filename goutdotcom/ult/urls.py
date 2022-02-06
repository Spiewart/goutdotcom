from django.urls import path

from .views import ULTCreate, ULTDetail, ULTUpdate

app_name = "ult"
urlpatterns = [
    path("create/", view=ULTCreate.as_view(), name="create"),
    path("<username>/create/", view=ULTCreate.as_view(), name="user-create"),
    path("<int:pk>/", view=ULTDetail.as_view(), name="detail"),
    path("<slug:slug>/", view=ULTDetail.as_view(), name="user-detail"),
    path("update/<int:pk>/", view=ULTUpdate.as_view(), name="update"),
    path("<slug:slug>/update/", view=ULTUpdate.as_view(), name="user-update"),
]
