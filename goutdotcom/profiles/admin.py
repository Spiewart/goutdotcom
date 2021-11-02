from django.contrib import admin

from .models import (
    ContraindicationsProfile,
    FamilyProfile,
    MedicalProfile,
    PatientProfile,
    SocialProfile,
)


# Register your models here.
class ContraindicationsProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "stroke",
        "heartattack",
        "bleed",
    )


class FamilyProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gout",
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


class SocialProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "alcohol",
        "fructose",
        "shellfish",
    )


admin.site.register(ContraindicationsProfile, ContraindicationsProfileAdmin)
admin.site.register(FamilyProfile, FamilyProfileAdmin)
admin.site.register(MedicalProfile, MedicalProfileAdmin)
admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(SocialProfile, SocialProfileAdmin)
