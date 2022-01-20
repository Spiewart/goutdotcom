from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


class ULTPlanHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "ultaid",
        "ppxaid",
        "goal_urate",
        "titration_lab_interval",
        "monitoring_lab_interval",
        "titrating",
        "last_titration",
        "pause",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


admin.site.register(ULTPlan, ULTPlanHistoryAdmin)
