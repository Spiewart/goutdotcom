from django.contrib import admin

from .models import *


class ULTAidAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "ult",
        "need",
        "want",
        "ckd",
        "XOI_interactions",
        "organ_transplant",
        "allopurinol_hypersensitivity",
        "febuxostat_hypersensitivity",
        "heartattack",
        "stroke",
        "decision_aid",
        "pk",
    )


admin.site.register(ULTAid, ULTAidAdmin)
