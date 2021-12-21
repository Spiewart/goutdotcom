from django.urls import path

from .views import ULTPlanCreate, ULTPlanDetail, ULTPlanUpdate

app_name = "ultplan"
urlpatterns = [
    path("create/", view=ULTPLanCreate.as_view(), name="create"),
    path("<int:pk>/", view=ULTPlanDetail.as_view(), name="detail"),
    path("update/<int:pk>/", view=ULTAidUpdate.as_view(), name="update"),
]
