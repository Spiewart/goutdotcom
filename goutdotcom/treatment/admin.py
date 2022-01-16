from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


# Register your models here.
class AllopurinolHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "ultplan",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class FebuxostatHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class NaproxenHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class CelecoxibHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class IbuprofenHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class PrednisoneHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "dose2",
        "freq2",
        "duration",
        "created",
        "flareaid",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class MethylprednisoloneHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class ProbenecidHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class ColchicineHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class MeloxicamHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "dose",
        "freq",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class TinctureoftimeHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "__str__",
        "user",
        "duration",
        "created",
        "modified",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class OthertreatHistoryAdmin(SimpleHistoryAdmin):
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
    history_list_display = ["status"]
    search_fields = ["user__username"]


admin.site.register(Allopurinol, AllopurinolHistoryAdmin)
admin.site.register(Febuxostat, FebuxostatHistoryAdmin)
admin.site.register(Ibuprofen, IbuprofenHistoryAdmin)
admin.site.register(Naproxen, NaproxenHistoryAdmin)
admin.site.register(Celecoxib, CelecoxibHistoryAdmin)
admin.site.register(Prednisone, PrednisoneHistoryAdmin)
admin.site.register(Methylprednisolone, MethylprednisoloneHistoryAdmin)
admin.site.register(Probenecid, ProbenecidHistoryAdmin)
admin.site.register(Colchicine, ColchicineHistoryAdmin)
admin.site.register(Meloxicam, MeloxicamHistoryAdmin)
admin.site.register(Tinctureoftime, TinctureoftimeHistoryAdmin)
admin.site.register(Othertreat, OthertreatHistoryAdmin)
