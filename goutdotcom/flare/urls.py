from django.urls import path

from .views import *

app_name = "flare"
urlpatterns = [
    path("ULT/create/", view=ULTCreate.as_view(), name="ult-create"),
    path("ULT/<int:pk>/", view=ULTdetail.as_view(), name="ult-detail"),
]
