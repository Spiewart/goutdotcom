from django.contrib import admin

from .models import *
# Register your models here.
class AllopurinolAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        "date_started",
        'date_ended',
        'dose',
        'pk',
    )
class FebuxostatAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        "date_started",
        'date_ended',
        'dose',
    )

admin.site.register(Allopurinol, AllopurinolAdmin)
admin.site.register(Febuxostat, FebuxostatAdmin)