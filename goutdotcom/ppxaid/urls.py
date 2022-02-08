from django.urls import path

from .views import PPxAidCreate, PPxAidDetail, PPxAidUpdate

app_name = "ppxaid"
urlpatterns = [
    path("<int:pk>/", view=PPxAidDetail.as_view(), name="detail"),
    path("<slug:slug>/", view=PPxAidDetail.as_view(), name="user-detail"),
    path("<slug:slug>/update/", view=PPxAidUpdate.as_view(), name="update"),
    path("create/", view=PPxAidCreate.as_view(), name="create"),
    path("create/ultaid/<int:pk>/", view=PPxAidCreate.as_view(), name="ultaid-create"),
    path("<slug:slug>/create/ultaid/<slug:ultaid>/", view=PPxAidCreate.as_view(), name="user-ultaid-create"),
]
