from django.urls import path
from gout import views

urlpatterns = [
    path('', views.index, name='index'),
    path('patient/', views.PatientListView.as_view(), name='patient'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('flares/<int:pk>/', views.FlareDetailView.as_view(), name='flare_detail'),
    path('flare_list/', views.FlareListView.as_view(), name='flare_list'),
    path('patientowners/', views.PatientOwnerView.as_view(), name='patient_owner'),
    path('patient/create/', views.PatientCreate.as_view(), name='patient_create'),
    path('patient/<int:pk>/update/', views.PatientUpdate.as_view(), name='patient_update'),
    path('patient/<int:pk>/delete/', views.PatientDelete.as_view(), name='patient_delete'),
]
