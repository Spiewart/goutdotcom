from django.contrib import admin

from .models import *
# Register your models here.

class WeightAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "units",
        "convert_pounds_to_kg",
        "altunit",
        "date_recorded",
        "created",
    )


admin.site.register(Weight, WeightAdmin)
