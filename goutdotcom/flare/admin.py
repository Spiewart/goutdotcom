from django.contrib import admin

from .models import *

class FlareAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'treatment',
        'urate',
        'pk',
    )

admin.site.register(Flare, FlareAdmin)
