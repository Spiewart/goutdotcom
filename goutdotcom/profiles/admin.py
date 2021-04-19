from django.contrib import admin

from .models import PatientProfile

# Register your models here.
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'picture',
        'date_of_birth',
        'age',
        'gender',
        'race',
        'weight',
        'height',
        'BMI_calculator',
        'drinks_per_week',
    )

admin.site.register(PatientProfile, PatientProfileAdmin)
