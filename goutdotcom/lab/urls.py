from django.urls import path

from .views import (
    IndexView,
    ALTUpdate,
    ASTUpdate,
    LabAbout,
    LabCreate,
    LabDetail,
    LabList,
    UrateUpdate,
    PlateletUpdate,
    WBCUpdate,
    HemoglobinUpdate,
    CreatinineUpdate,
)

app_name = "lab"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("about/<lab>/", view=LabAbout.as_view(), name="about"),
    path("create/<lab>/", view=LabCreate.as_view(), name="lab-create"),
    path("list/<lab>/", view=LabList.as_view(), name="lab-list"),
    path("<lab>/<int:pk>/", view=LabDetail.as_view(), name="lab-detail"),
    path("urate/<int:pk>/update/", view=UrateUpdate.as_view(), name="urate-update"),    
    path("ALT/<int:pk>/update/", view=ALTUpdate.as_view(), name="ALT-update"),   
    path("AST/<int:pk>/update/", view=ASTUpdate.as_view(), name="AST-update"),  
    path("platelet/<int:pk>/update/", view=PlateletUpdate.as_view(), name="platelet-update"),   
    path("WBC/<int:pk>/update/", view=WBCUpdate.as_view(), name="WBC-update"),   
    path("hemoglobin/<int:pk>/update/", view=HemoglobinUpdate.as_view(), name="hemoglobin-update"),  
    path("creatinine/<int:pk>/update/", view=CreatinineUpdate.as_view(), name="creatinine-update"),   
]
