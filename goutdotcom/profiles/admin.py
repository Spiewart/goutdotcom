from django.contrib import admin

from .models import ContraindicationsProfile, MedicalProfile, PatientProfile


# Register your models here.
class ContraindicationsProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "stroke",
        "heartattack",
        "bleed",
    )


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
    )


admin.site.register(ContraindicationsProfile, ContraindicationsProfileAdmin)
admin.site.register(MedicalProfile, MedicalProfileAdmin)
admin.site.register(PatientProfile, PatientProfileAdmin)
