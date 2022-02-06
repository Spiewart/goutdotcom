from django.urls import path

from .views import ULTAidCreate, ULTAidDetail, ULTAidUpdate

app_name = "ultaid"
urlpatterns = [
    path("create/", view=ULTAidCreate.as_view(), name="create"),
    path("create/ult/<int:ult>/", view=ULTAidCreate.as_view(), name="ult-create"),
    path("<username>/create/", view=ULTAidCreate.as_view(), name="user-create"),
    path("<username>/create/ult/<slug:ult>/", view=ULTAidCreate.as_view(), name="user-ult-create"),
    path("<int:pk>/", view=ULTAidDetail.as_view(), name="detail"),
    path("<slug:slug>/", view=ULTAidDetail.as_view(), name="user-detail"),
    path("update/<int:pk>/", view=ULTAidUpdate.as_view(), name="update"),
]
