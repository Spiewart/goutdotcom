from django.contrib import admin

from .models import *
# Register your models here.
class AllopurinolAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
    )
class FebuxostatAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
    )

class NaproxenAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
    )

class CelecoxibAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
    )

class IbuprofenAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
    )

class PrednisoneAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
    )

class MethylprednisoloneAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
    )

class ProbenecidAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
    )

class ColchicineAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'dose',
        'freq',
        'duration_calc',
        'pk',
    )
admin.site.register(Allopurinol, AllopurinolAdmin)
admin.site.register(Febuxostat, FebuxostatAdmin)
admin.site.register(Ibuprofen, IbuprofenAdmin)
admin.site.register(Naproxen, NaproxenAdmin)
admin.site.register(Celecoxib, CelecoxibAdmin)
admin.site.register(Prednisone, PrednisoneAdmin)
admin.site.register(Methylprednisolone, MethylprednisoloneAdmin)
admin.site.register(Probenecid, ProbenecidAdmin)
admin.site.register(Colchicine, ColchicineAdmin)
