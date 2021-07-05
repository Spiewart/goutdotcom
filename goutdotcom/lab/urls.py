from django.apps import apps
from django.urls import path
from django.views.generic import TemplateView

from . import views

from .views import (
    IndexView,
    ALTDetail,
    ALTList,
    ALTUpdate,
    ASTDetail,
    ASTList,
    ASTUpdate,
    LabAbout,
    LabCreate,
    UrateDetail,
    UrateList,
    UrateUpdate,
    PlateletDetail,
    PlateletList,
    PlateletUpdate,
    WBCDetail,
    WBCList,
    WBCUpdate,
    HemoglobinDetail,
    HemoglobinList,
    HemoglobinUpdate,
    CreatinineDetail,
    CreatinineList,
    CreatinineUpdate,
)

app_name = "lab"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("about/<lab>/", view=LabAbout.as_view(), name="about"),
    path("create/<lab>/", view=LabCreate.as_view(), name="lab-create"),
    path("urate/<int:pk>/update/", view=UrateUpdate.as_view(), name="urate-update"),    
    path("urate/", view=UrateList.as_view(), name="urate-list"),
    path("urate/<int:pk>/", view=UrateDetail.as_view(), name="urate-detail"),
    path("ALT/<int:pk>/update/", view=ALTUpdate.as_view(), name="ALT-update"),   
    path("ALT/", view=ALTList.as_view(), name="ALT-list"),
    path("ALT/<int:pk>/", view=ALTDetail.as_view(), name="ALT-detail"),
    path("AST/<int:pk>/update/", view=ASTUpdate.as_view(), name="AST-update"),  
    path("AST/", view=ASTList.as_view(), name="AST-list"),
    path("AST/<int:pk>/", view=ASTDetail.as_view(), name="AST-detail"),
    path("platelet/<int:pk>/update/", view=PlateletUpdate.as_view(), name="platelet-update"),   
    path("platelet/", view=PlateletList.as_view(), name="platelet-list"),
    path("platelet/<int:pk>/", view=PlateletDetail.as_view(), name="platelet-detail"),
    path("WBC/<int:pk>/update/", view=WBCUpdate.as_view(), name="WBC-update"),   
    path("WBC/", view=WBCList.as_view(), name="WBC-list"),
    path("WBC/<int:pk>/", view=WBCDetail.as_view(), name="WBC-detail"),
    path("hemoglobin/<int:pk>/update/", view=HemoglobinUpdate.as_view(), name="hemoglobin-update"),  
    path("hemoglobin/", view=HemoglobinList.as_view(), name="hemoglobin-list"),
    path("hemoglobin/<int:pk>/", view=HemoglobinDetail.as_view(), name="hemoglobin-detail"),
    path("creatinine/<int:pk>/update/", view=CreatinineUpdate.as_view(), name="creatinine-update"),   
    path("creatinine/", view=CreatinineList.as_view(), name="creatinine-list"),
    path("creatinine/<int:pk>/", view=CreatinineDetail.as_view(), name="creatinine-detail"),
]
