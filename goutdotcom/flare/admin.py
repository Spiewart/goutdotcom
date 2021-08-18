from django.contrib import admin

from .models import *

class FlareAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'treatment',
        'urate',
        'created',
        'modified',
        'pk',
    )

admin.site.register(Flare, FlareAdmin)
