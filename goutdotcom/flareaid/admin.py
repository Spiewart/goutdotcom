from django.contrib import admin

# Register your models here.
from .models import *


class FlareAidAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "flare",
        "perfect_health",
        "monoarticular",
        "anticoagulation",
        "bleed",
        "ckd",
        "colchicine_interactions",
        "diabetes",
        "heartattack",
        "ibd",
        "osteoporosis",
        "stroke",
        "monoarticular_aid",
        "decision_aid",
        "pk",
    )


admin.site.register(FlareAid, FlareAidAdmin)
