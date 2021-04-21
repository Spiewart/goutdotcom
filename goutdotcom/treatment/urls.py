from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AllopurinolDetail,
    FebuxostatDetail,
)

app_name = "treatment"
urlpatterns = [
    path("", TemplateView.as_view(template_name="treatment/index.html"), name="index"),
    path("flare/", TemplateView.as_view(template_name="treatment/flare.html"), name="flare"),
    path("prevention/", TemplateView.as_view(template_name="treatment/prevention.html"), name="prevention"),
    path("allopurinol/<slug:med_slug>/", view=AllopurinolDetail.as_view(), name="allopurinol-detail"),
    path("febuxostat/<int:pk>/", view=FebuxostatDetail.as_view(), name="febuxostat-detail"),
]