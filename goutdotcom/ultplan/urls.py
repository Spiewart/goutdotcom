from django.urls import path

from .views import ULTPlanCreate, ULTPlanDetail

app_name = "ultplan"
urlpatterns = [
    path("create/", view=ULTPlanCreate.as_view(), name="create"),
    path("<int:pk>/", view=ULTPlanDetail.as_view(), name="detail"),
]
