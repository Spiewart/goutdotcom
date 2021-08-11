from django.urls import path

from .views import *

app_name = "vitals"

urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("<vital>/<int:pk>/", view=VitalDetail.as_view(), name="detail"),
    path("create/<vital>/", view=VitalCreate.as_view(), name="create"),
    path("create/<vital>/<int:pk>/", view=VitalUpdate.as_view(), name="update"),
    path("list/<vital>/", view=VitalList.as_view(), name="list"),
]
