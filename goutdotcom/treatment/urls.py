from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AllopurinolDetail,
    AllopurinolCreate,
    AllopurinolUpdate,
    ColchicineDetail,
    ColchicineCreate,
    ColchicineUpdate,
    FebuxostatDetail,
    FebuxostatCreate,
    FebuxostatUpdate,
)

app_name = "treatment"
urlpatterns = [
    path("", TemplateView.as_view(template_name="treatment/index.html"), name="index"),
    path("flare/", TemplateView.as_view(template_name="treatment/flare.html"), name="flare"),
    path("prevention/", TemplateView.as_view(template_name="treatment/prevention.html"), name="prevention"),
    path("allopurinol/<int:pk>/", view=AllopurinolDetail.as_view(), name="allopurinol-detail"),
    path("allopurinol/create/", view=AllopurinolCreate.as_view(), name="allopurinol-create"),
    path("allopurinol/<int:pk>/update/", view=AllopurinolUpdate.as_view(), name="allopurinol-update"),
    path("colchicine/<int:pk>/", view=ColchicineDetail.as_view(), name="colchicine-detail"),
    path("colchicine/create/", view=ColchicineCreate.as_view(), name="colchicine-create"),
    path("colchicine/<int:pk>/update/", view=ColchicineUpdate.as_view(), name="colchicine-update"),
    path("febuxostat/<int:pk>/", view=FebuxostatDetail.as_view(), name="febuxostat-detail"),
    path("febuxostat/create/", view=FebuxostatCreate.as_view(), name="febuxostat-create"),
    path("febuxostat/<int:pk>/update/", view=FebuxostatUpdate.as_view(), name="febuxostat-update"),
]