from django.urls import path

from .views import ULTCreate, ULTDetail, ULTUpdate

app_name = "ult"
urlpatterns = [
    path("create/", view=ULTCreate.as_view(), name="create"),
    path("<int:pk>/", view=ULTDetail.as_view(), name="detail"),
    path("update/<int:pk>/", view=ULTUpdate.as_view(), name="update"),
]
