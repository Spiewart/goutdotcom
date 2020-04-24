from django.contrib import admin
from .models import Patient, Flare, Info
from django.contrib.auth.models import User, Group

admin.site.site_url = 'http://127.0.0.1:8000/gout/'
# Register your models here.

admin.site.register(Flare)
admin.site.register(Info)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'sexes', 'gender', 'email', 'owner')
    list_filter = ('last_name', 'first_name')
