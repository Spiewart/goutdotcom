from django.contrib import admin

from .models import *


# Register your models here.
class ULTAidAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
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
