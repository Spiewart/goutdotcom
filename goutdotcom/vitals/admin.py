from django.contrib import admin

from .models import *

# Register your models here.


class WeightAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "units",
        "weight_in_kgs",
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
        "height_in_meters",
        "altunit",
        "height_in_feet",
        "date_recorded",
        "created",
        "pk",
    )


admin.site.register(Weight, WeightAdmin)
admin.site.register(Height, HeightAdmin)
