from django.urls import path

from .views import ULTPlanBluePrint, ULTPlanCreate, ULTPlanDelete, ULTPlanDetail

app_name = "ultplan"
urlpatterns = [
    path("blueprint/", view=ULTPlanBluePrint.as_view(), name="blueprint"),
    path("<username>/create/", view=ULTPlanCreate.as_view(), name="create"),
    path("<slug:slug>/", view=ULTPlanDetail.as_view(), name="detail"),
    path("delete/<slug:slug>/", view=ULTPlanDelete.as_view(), name="delete"),
]
