from django.urls import path

from .views import *

app_name = "treatment"
urlpatterns = [
    path("about/", view=About.as_view(), name="about"),
    path("about/corticosteroids/", view=AboutCorticosteroids.as_view(), name="about-corticosteroids"),
    path("about/flare/", view=AboutFlare.as_view(), name="about-flare"),
    path("about/nsaids/", view=AboutNSAIDs.as_view(), name="about-NSAIDs"),
    path("about/prophylaxis/", view=AboutProphylaxis.as_view(), name="about-prophylaxis"),
    path("about/ult/", view=AboutULT.as_view(), name="about-ult"),
    path("about/<treatment>", view=TreatmentAbout.as_view(), name="about"),
    path("<slug:username>/", view=IndexView.as_view(), name="index"),
    path("<slug:username>/flare/", FlareView.as_view(), name="flare"),
    path("<slug:username>/prophylaxis/", ProphylaxisView.as_view(), name="prophylaxis"),
    path("<slug:username>/ult/", ULTView.as_view(), name="ult"),
    path("<treatment>/<slug:slug>/", view=TreatmentDetail.as_view(), name="detail"),
    path("<slug:username>/list/<treatment>/", view=TreatmentList.as_view(), name="list"),
    path("<slug:username>/create/<treatment>/", view=TreatmentCreate.as_view(), name="create"),
    path(
        "<slug:username>/create/flareaid/<slug:slug>/<treatment>/",
        view=FlareAidTreatmentCreate.as_view(),
        name="flareaid-create",
    ),
    path("<slug:username>/create/ppx/<treatment>/", view=ProphylaxisCreate.as_view(), name="prophylaxis-create"),
    path("update/<treatment>/<slug:slug>/", view=TreatmentUpdate.as_view(), name="update"),
]
