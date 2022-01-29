from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import FamilyProfile, MedicalProfile, PatientProfile, SocialProfile


# Register your models here.
class FamilyProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "gout",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class MedicalProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
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
        "organ_transplant",
        "osteoporosis",
        "stroke",
        "urate_kidney_stones",
        "tophi",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class PatientProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "date_of_birth",
        "get_age",
        "gender",
        "race",
        "weight",
        "height",
        "BMI_calculator",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


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


class SocialProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "alcohol",
        "fructose",
        "shellfish",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


admin.site.register(FamilyProfile, FamilyProfileHistoryAdmin)
admin.site.register(MedicalProfile, MedicalProfileHistoryAdmin)
admin.site.register(PatientProfile, PatientProfileHistoryAdmin)
admin.site.register(PatientProfile, ProviderProfileHistoryAdmin)
admin.site.register(SocialProfile, SocialProfileHistoryAdmin)
