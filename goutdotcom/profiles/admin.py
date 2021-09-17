from django.contrib import admin

from .models import MedicalProfile, PatientProfile


# Register your models here.
class MedicalProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "CKD",
        "hypertension",
        "CHF",
        "diabetes",
        "organ_transplant",
        "urate_kidney_stones",
    )


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "picture",
        "date_of_birth",
        "get_age",
        "gender",
        "race",
        "weight",
        "height",
        "BMI_calculator",
        "drinks_per_week",
    )


admin.site.register(MedicalProfile, MedicalProfileAdmin)
admin.site.register(PatientProfile, PatientProfileAdmin)
