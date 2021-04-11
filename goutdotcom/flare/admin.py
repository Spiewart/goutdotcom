from django.contrib import admin

from .models import *


class ULTAdmin(admin.ModelAdmin):
    list_display = (
        "num_flares",
        "freq_flares",
        "first_flare",
        "erosions",
        "tophi",
        "stones",
        "ckd",
        "uric_acid",
        "calculator",
    )


admin.site.register(ULT, ULTAdmin)
