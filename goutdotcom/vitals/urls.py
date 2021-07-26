from django.urls import path

from .views import *

app_name = "vitals"
urlpatterns = [
    ###path("", view=IndexView.as_view(), name="index"),
    path("<vital>/<int:pk>/", view=VitalDetail.as_view(), name="detail"),
]
