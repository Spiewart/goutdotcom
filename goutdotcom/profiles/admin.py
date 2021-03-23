from django.contrib import admin

from .models import PatientProfile

# Register your models here.
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'picture',
    )

admin.site.register(PatientProfile, PatientProfileAdmin)