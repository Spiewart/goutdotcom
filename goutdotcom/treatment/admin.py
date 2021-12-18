from django.contrib import admin

from .models import *


# Register your models here.
class AllopurinolAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class FebuxostatAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class NaproxenAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class CelecoxibAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class IbuprofenAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class PrednisoneAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "flareaid",
        "modified",
        "pk",
    )


class MethylprednisoloneAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class ProbenecidAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class ColchicineAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class MeloxicamAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )


class TinctureoftimeAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "duration",
        "created",
        "modified",
        "pk",
    )


class OthertreatAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "name",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
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
admin.site.register(Meloxicam, MeloxicamAdmin)
admin.site.register(Tinctureoftime, TinctureoftimeAdmin)
admin.site.register(Othertreat, OthertreatAdmin)
