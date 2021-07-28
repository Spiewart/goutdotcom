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
        "pk",
    )


class HeightAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "units",
        "convert_inches_to_meters",
        "altunit",
        "convert_inches_to_feet",
        "date_recorded",
        "created",
        "pk",
    )

admin.site.register(Weight, WeightAdmin)
admin.site.register(Height, HeightAdmin)
