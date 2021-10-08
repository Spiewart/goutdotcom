from django.urls import path

from .views import (
    AboutFlares,
    DecisionAidCreate,
    DecisionAidDetail,
    DecisionAidForm,
    DecisionAidList,
    DecisionAidUpdate,
    FlareCreate,
    FlareDetail,
    FlareList,
    FlareUpdate,
)

app_name = "flare"
urlpatterns = [
    path("about/", view=AboutFlares.as_view(), name="about"),
    path("<int:pk>/", view=FlareDetail.as_view(), name="detail"),
    path("<int:pk>/update/", view=FlareUpdate.as_view(), name="update"),
    path("create/", view=FlareCreate.as_view(), name="create"),
    path("decisionaid/create", view=DecisionAidCreate.as_view(), name="decisionaid-create"),
    path("decisionaid/<int:pk>/", view=DecisionAidDetail.as_view(), name="decisionaid-detail"),
    path("decisionaid/<int:pk>/update", view=DecisionAidCreate.as_view(), name="decisionaid-update"),
    path("decisionaid/", view=DecisionAidList.as_view(), name="decisionaid-list"),
    path("", view=FlareList.as_view(), name="list"),
]
