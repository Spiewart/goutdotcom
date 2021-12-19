from django.contrib import admin

from .models import *


class PPxAidAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "pk",
    )


admin.site.register(PPxAid, PPxAidAidAdmin)
