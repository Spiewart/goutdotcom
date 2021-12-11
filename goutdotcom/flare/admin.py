from django.contrib import admin

from .models import *


class FlareAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "monoarticular",
        "male",
        "prior_gout",
        "onset",
        "firstmtp",
        "location",
        "angina",
        "hypertension",
        "heartattack",
        "CHF",
        "stroke",
        "PVD",
        "duration",
        "treatment",
        "urate",
        "created",
        "modified",
        "pk",
    )


admin.site.register(Flare, FlareAdmin)
