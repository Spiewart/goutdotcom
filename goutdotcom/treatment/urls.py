from django.urls import path

from .views import *

app_name = "treatment"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("dashboard/", view=DashboardView.as_view(), name="dashboard"),
    path("flare/", FlareView.as_view(), name="flare"),
    path("ult/", ULTView.as_view(), name="ult"),
    path("<treatment>/", view=TreatmentList.as_view(), name="list"),
    path("<treatment>/<int:pk>/", view=TreatmentDetail.as_view(), name="detail"),
    path("create/<treatment>/", view=TreatmentCreate.as_view(), name="create"),
    path("update/<treatment>/<int:pk>/", view=TreatmentUpdate.as_view(), name="update"),

]
