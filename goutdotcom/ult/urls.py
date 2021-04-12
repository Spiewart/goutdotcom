from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import (
    ULTCreate,
    ULTDetail,
)


app_name = "ult"
urlpatterns = [
    path("ULT/create/", view=ULTCreate.as_view(), name="create"),
    path("ULT/<int:pk>/", view=ULTDetail.as_view(), name="detail"),
    path("", TemplateView.as_view(template_name="ult/index.html"), name="index"),
]
