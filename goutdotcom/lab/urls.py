from django.urls import path
from django.views.generic import TemplateView

from .views import (
    IndexView,
    log,
    ALTCreate,
    ALTDetail,
    ALTList,
    ASTCreate,
    ASTDetail,
    ASTList,
    UrateCreate,
    UrateDetail,
    UrateList,
)

app_name = "lab"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("log/", TemplateView.as_view(template_name='lab/log.html'), name="log"),
    path("urate/", view=UrateList.as_view(), name="urate-list"),
    path("urate/create/", view=UrateCreate.as_view(), name="urate-create"),
    path("urate/<int:pk>/", view=UrateDetail.as_view(), name="urate-detail"),
    path("ALT/", view=ALTList.as_view(), name="ALT-list"),
    path("ALT/create/", view=ALTCreate.as_view(), name="ALT-create"),
    path("ALT/<int:pk>/", view=ALTDetail.as_view(), name="ALT-detail"),
    path("AST/", view=ASTList.as_view(), name="AST-list"),
    path("AST/create/", view=ASTCreate.as_view(), name="AST-create"),
    path("AST/<int:pk>/", view=ASTDetail.as_view(), name="AST-detail"),
]
