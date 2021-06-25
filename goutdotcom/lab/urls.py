from django.urls import path
from django.views.generic import TemplateView

from . import views

from .views import (
    IndexView,
    ALTAbout,
    ALTCreate,
    ALTDetail,
    ALTList,
    ALTUpdate,
    ASTAbout,
    ASTCreate,
    ASTDetail,
    ASTList,
    ASTUpdate,
    UrateAbout,
    UrateCreate,
    UrateDetail,
    UrateList,
    UrateUpdate,
    PlateletAbout,
    PlateletCreate,
    PlateletDetail,
    PlateletList,
    PlateletUpdate,
    WBCAbout,
    WBCCreate,
    WBCDetail,
    WBCList,
    WBCUpdate,
    HemoglobinAbout,
    HemoglobinCreate,
    HemoglobinDetail,
    HemoglobinList,
    HemoglobinUpdate,
    CreatinineAbout,
    CreatinineCreate,
    CreatinineDetail,
    CreatinineList,
    CreatinineUpdate,
)

app_name = "lab"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("about/", views.LabAbout, name="lab-about"),
    path("urate/<int:pk>/update/", view=UrateUpdate.as_view(), name="urate-update"),    
    path("urate/", view=UrateList.as_view(), name="urate-list"),
    path("urate/about/", view=UrateAbout.as_view(), name="urate-about"), 
    path("urate/create/", view=UrateCreate.as_view(), name="urate-create"),
    path("urate/<int:pk>/", view=UrateDetail.as_view(), name="urate-detail"),
    path("ALT/<int:pk>/update/", view=ALTUpdate.as_view(), name="ALT-update"),    
    path("ALT/", view=ALTList.as_view(), name="ALT-list"),
    path("ALT/about/", view=ALTAbout.as_view(), name="alt-about"), 
    path("ALT/create/", view=ALTCreate.as_view(), name="ALT-create"),
    path("ALT/<int:pk>/", view=ALTDetail.as_view(), name="ALT-detail"),
    path("AST/<int:pk>/update/", view=ASTUpdate.as_view(), name="AST-update"),    
    path("AST/", view=ASTList.as_view(), name="AST-list"),
    path("AST/about/", view=ASTAbout.as_view(), name="ast-about"), 
    path("AST/create/", view=ASTCreate.as_view(), name="AST-create"),
    path("AST/<int:pk>/", view=ASTDetail.as_view(), name="AST-detail"),
    path("platelet/<int:pk>/update/", view=PlateletUpdate.as_view(), name="platelet-update"),    
    path("platelet/", view=PlateletList.as_view(), name="platelet-list"),
    path("platelet/about/", view=PlateletAbout.as_view(), name="platelet-about"), 
    path("platelet/create/", view=PlateletCreate.as_view(), name="platelet-create"),
    path("platelet/<int:pk>/", view=PlateletDetail.as_view(), name="platelet-detail"),
    path("WBC/<int:pk>/update/", view=WBCUpdate.as_view(), name="WBC-update"),
    path("WBC/", view=WBCList.as_view(), name="WBC-list"),
    path("WBC/about/", view=WBCAbout.as_view(), name="WBC-about"), 
    path("WBC/create/", view=WBCCreate.as_view(), name="WBC-create"),
    path("WBC/<int:pk>/", view=WBCDetail.as_view(), name="WBC-detail"),
    path("hemoglobin/<int:pk>/update/", view=HemoglobinUpdate.as_view(), name="hemoglobin-update"),
    path("hemoglobin/", view=HemoglobinList.as_view(), name="hemoglobin-list"),
    path("hemoglobin/about/", view=HemoglobinAbout.as_view(), name="hemoglobin-about"), 
    path("hemoglobin/create/", view=HemoglobinCreate.as_view(), name="hemoglobin-create"),
    path("hemoglobin/<int:pk>/", view=HemoglobinDetail.as_view(), name="hemoglobin-detail"),
    path("creatinine/<int:pk>/update/", view=CreatinineUpdate.as_view(), name="creatinine-update"),
    path("creatinine/", view=CreatinineList.as_view(), name="creatinine-list"),
    path("creatinine/about/", view=CreatinineAbout.as_view(), name="creatinine-about"), 
    path("creatinine/create/", view=CreatinineCreate.as_view(), name="creatinine-create"),
    path("creatinine/<int:pk>/", view=CreatinineDetail.as_view(), name="creatinine-detail"),
]
