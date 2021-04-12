from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "flare"
urlpatterns = [
    path("", TemplateView.as_view(template_name="flare/index.html"), name="index"),
]
