from django.urls import path
from gout import views

urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.PatientListView.as_view(), name='patients'),
    path('flares/<int:pk>/', views.FlareDetailView.as_view(), name='flares'),
    path('flare_list/', views.FlareListView.as_view(), name='flare_list'),
    path('patientowners/', views.PatientOwnerView.as_view(), name='patient_owner'),
]
