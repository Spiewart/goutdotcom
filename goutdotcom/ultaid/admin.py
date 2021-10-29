from django.contrib import admin

from .models import *


# Register your models here.
class ULTAidAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'ckd',
        'stage',
        'dialysis',
        'XOI_interactions',
        'organ_transplant',
        'allopurinol_hypersensitivity',
        'febuxostat_hypersensitivity',
        'MADE',
        'decision_aid',
        'pk',
    )
admin.site.register(ULTAid, ULTAidAdmin)
