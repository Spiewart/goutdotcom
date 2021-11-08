from django.contrib import admin

from .models import *


class ULTAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "pk",
        "num_flares",
        "freq_flares",
        "erosions",
        "tophi",
        "stones",
        "ckd",
        "hyperuricemia",
        "calculator",
        "modified",
    )
    ordering = ("-modified",)


admin.site.register(ULT, ULTAdmin)
