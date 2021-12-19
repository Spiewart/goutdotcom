from django.urls import path

from .views import PPxAidCreate, PPxAidDetail, PPxAidUpdate

app_name = "ppxaid"
urlpatterns = [
    path("<int:pk>/", view=PPxAidDetail.as_view(), name="detail"),
    path("<int:pk>/update/", view=PPxAidUpdate.as_view(), name="update"),
    path("<int:pk>/update/ultaid/<int:ultaid>/", view=PPxAidCreate.as_view(), name="ultaid-update"),
    path("create/", view=PPxAidCreate.as_view(), name="create"),
    path("create/ultaid/<int:ultaid>/", view=PPxAidCreate.as_view(), name="ultaid-create"),
]
