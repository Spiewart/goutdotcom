from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *

# Register your models here.


class UrateHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "ultplan",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class ALTHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class ASTHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class LabCheckHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "ultplan",
        "pk",
        "alt",
        "ast",
        "creatinine",
        "hemoglobin",
        "platelet",
        "wbc",
        "urate",
        "due",
        "completed",
        "completed_date",
        # "overdue",
        "created",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class PlateletHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class WBCHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class HemoglobinHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class CreatinineHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "eGFR_calculator",
        "date_drawn",
        "created",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


admin.site.register(Urate, UrateHistoryAdmin)
admin.site.register(ALT, ALTHistoryAdmin)
admin.site.register(AST, ASTHistoryAdmin)
admin.site.register(LabCheck, LabCheckHistoryAdmin)
admin.site.register(Platelet, PlateletHistoryAdmin)
admin.site.register(WBC, WBCHistoryAdmin)
admin.site.register(Hemoglobin, HemoglobinHistoryAdmin)
admin.site.register(Creatinine, CreatinineHistoryAdmin)
