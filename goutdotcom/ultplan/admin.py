from django.contrib import admin

from .models import *


class ULTPlanAdmin(admin.ModelAdmin):
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
        "pk",
    )


admin.site.register(ULTPlan, ULTPlanAdmin)
