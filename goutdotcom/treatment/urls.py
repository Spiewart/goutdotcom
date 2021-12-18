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
    path("dashboard/", view=DashboardView.as_view(), name="dashboard"),
    path("flare/", FlareView.as_view(), name="flare"),
    path("prophylaxis/", ProphylaxisView.as_view(), name="prophylaxis"),
    path("ult/", ULTView.as_view(), name="ult"),
    path("<treatment>/", view=TreatmentList.as_view(), name="list"),
    path("<treatment>/<int:pk>/", view=TreatmentDetail.as_view(), name="detail"),
    path("create/<treatment>/", view=TreatmentCreate.as_view(), name="create"),
    path("create/flareaid/<int:pk>/<treatment>/", view=FlareAidTreatmentCreate.as_view(), name="flareaid-create"),
    path("create/ppx/<treatment>/", view=ProphylaxisCreate.as_view(), name="prophylaxis-create"),
    path("update/<treatment>/<int:pk>/", view=TreatmentUpdate.as_view(), name="update"),
]
