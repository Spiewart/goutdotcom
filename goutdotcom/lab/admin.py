from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


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

class BaselineALTHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
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

class BaselineASTHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
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

class BaselineCreatinineHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "eGFR_calculator",
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

class BaselineHemoglobinHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
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

class BaselinePlateletHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
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

class BaselineWBCHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]




admin.site.register(Urate, UrateHistoryAdmin)
admin.site.register(ALT, ALTHistoryAdmin)
admin.site.register(BaselineALT, BaselineALTHistoryAdmin)
admin.site.register(AST, ASTHistoryAdmin)
admin.site.register(BaselineAST, BaselineASTHistoryAdmin)
admin.site.register(Creatinine, CreatinineHistoryAdmin)
admin.site.register(BaselineCreatinine, BaselineCreatinineHistoryAdmin)
admin.site.register(Hemoglobin, HemoglobinHistoryAdmin)
admin.site.register(BaselineHemoglobin, BaselineHemoglobinHistoryAdmin)
admin.site.register(LabCheck, LabCheckHistoryAdmin)
admin.site.register(Platelet, PlateletHistoryAdmin)
admin.site.register(BaselinePlatelet, BaselinePlateletHistoryAdmin)
admin.site.register(WBC, WBCHistoryAdmin)
admin.site.register(BaselineWBC, BaselineWBCHistoryAdmin)


