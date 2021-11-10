from django.contrib import admin

from .models import FamilyProfile, MedicalProfile, PatientProfile, SocialProfile


# Register your models here.
class FamilyProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gout",
    )


class MedicalProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "anticoagulation",
        "bleed",
        "CHF",
        "CKD",
        "colchicine_interactions",
        "diabetes",
        "erosions",
        "hypertension",
        "hyperuricemia",
        "IBD",
        "organ_transplant",
        "osteoporosis",
        "stroke",
        "urate_kidney_stones",
        "tophi",
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


admin.site.register(FamilyProfile, FamilyProfileAdmin)
admin.site.register(MedicalProfile, MedicalProfileAdmin)
admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(SocialProfile, SocialProfileAdmin)
