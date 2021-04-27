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
    IbuprofenCreate,
    IbuprofenDetail,
    IbuprofenUpdate,
    IndexView,
    CelecoxibCreate,
    CelecoxibDetail,
    CelecoxibUpdate,
    NaproxenCreate,
    NaproxenDetail,
    NaproxenUpdate,
    MeloxicamCreate,
    MeloxicamDetail,
    MeloxicamUpdate,
    PrednisoneCreate,
    PrednisoneDetail,
    PrednisoneUpdate,
    MethylprednisoloneDetail,
    MethylprednisoloneCreate,
    MethylprednisoloneUpdate,
    ProbenecidDetail,
    ProbenecidCreate,
    ProbenecidUpdate,
)

app_name = "treatment"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
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
    path("ibuprofen/<int:pk>/", view=IbuprofenDetail.as_view(), name="ibuprofen-detail"),
    path("ibuprofen/create/", view=IbuprofenCreate.as_view(), name="ibuprofen-create"),
    path("ibuprofen/<int:pk>/update/", view=IbuprofenUpdate.as_view(), name="ibuprofen-update"),
    path("naproxen/<int:pk>/", view=NaproxenDetail.as_view(), name="naproxen-detail"),
    path("naproxen/create/", view=NaproxenCreate.as_view(), name="naproxen-create"),
    path("naproxen/<int:pk>/update/", view=NaproxenUpdate.as_view(), name="naproxen-update"),
    path("celecoxib/<int:pk>/", view=CelecoxibDetail.as_view(), name="celecoxib-detail"),
    path("celecoxib/create/", view=CelecoxibCreate.as_view(), name="celecoxib-create"),
    path("celecoxib/<int:pk>/update/", view=CelecoxibUpdate.as_view(), name="celecoxib-update"),
    path("meloxicam/<int:pk>/", view=MeloxicamDetail.as_view(), name="meloxicam-detail"),
    path("meloxicam/create/", view=MeloxicamCreate.as_view(), name="meloxicam-create"),
    path("meloxicam/<int:pk>/update/", view=MeloxicamUpdate.as_view(), name="meloxicam-update"),
    path("prednisone/<int:pk>/", view=PrednisoneDetail.as_view(), name="prednisone-detail"),
    path("prednisone/create/", view=PrednisoneCreate.as_view(), name="prednisone-create"),
    path("prednisone/<int:pk>/update/", view=PrednisoneUpdate.as_view(), name="prednisone-update"),
    path("probenecid/<int:pk>/", view=ProbenecidDetail.as_view(), name="probenecid-detail"),
    path("probenecid/create/", view=ProbenecidCreate.as_view(), name="probenecid-create"),
    path("probenecid/<int:pk>/update/", view=ProbenecidUpdate.as_view(), name="probenecid-update"),
    path("methylprednisolone/<int:pk>/", view=MethylprednisoloneDetail.as_view(), name="methylprednisolone-detail"),
    path("methylprednisolone/create/", view=MethylprednisoloneCreate.as_view(), name="methylprednisolone-create"),
    path("methylprednisolone/<int:pk>/update/", view=MethylprednisoloneUpdate.as_view(), name="methylprednisolone-update"),
]
