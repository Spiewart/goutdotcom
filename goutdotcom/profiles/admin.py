from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    FamilyProfile,
    MedicalProfile,
    PatientProfile,
    ProviderProfile,
    SocialProfile,
)


# Register your models here.
class FamilyProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "slug",
        "gout",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]
    prepopulated_fields = {
        "slug": ("user",),
    }


class MedicalProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "anemia",
        "angina",
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
        "leukocytosis",
        "leukopenia",
        "organ_transplant",
        "osteoporosis",
        "stroke",
        "urate_kidney_stones",
        "tophi",
        "transaminitis",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]
    prepopulated_fields = {
        "slug": ("user",),
    }


class PatientProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "provider",
        "patient_id",
        "pk",
        "date_of_birth",
        "age",
        "gender",
        "race",
        "weight",
        "height",
        "BMI",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]
    prepopulated_fields = {
        "slug": ("user",),
    }


class ProviderProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "organization",
        "titration_lab_interval",
        "monitoring_lab_interval",
        "urgent_lab_interval",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]
    prepopulated_fields = {
        "slug": ("user",),
    }


class SocialProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "alcohol",
        "fructose",
        "shellfish",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]
    prepopulated_fields = {
        "slug": ("user",),
    }


admin.site.register(FamilyProfile, FamilyProfileHistoryAdmin)
admin.site.register(MedicalProfile, MedicalProfileHistoryAdmin)
admin.site.register(PatientProfile, PatientProfileHistoryAdmin)
admin.site.register(ProviderProfile, ProviderProfileHistoryAdmin)
admin.site.register(SocialProfile, SocialProfileHistoryAdmin)
