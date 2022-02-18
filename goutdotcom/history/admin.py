from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *

class AlcoholHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "number",
        "wine",
        "beer",
        "liquor",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class AllopurinolHypersensitivityHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "rash",
        "transaminitis",
        "cytopenia",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class AnemiaHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "baseline",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class AnginaHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class AnticoagulationHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date",
        "warfarin",
        "apixaban",
        "rivaroxaban",
        "clopidogrel",
        "created",
        "pk",
    )

    history_list_display = ["status"]
    search_fields = ["user__username"]

class BleedHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "number",
        "date",
        "GIB",
        "CNS",
        "transfusion",
        "created",
        "pk",
    )

    history_list_display = ["status"]
    search_fields = ["user__username"]

class CHFHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "systolic",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class CKDHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "baseline",
        "stage",
        "dialysis",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class ColchicineInteractionsHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "clarithromycin",
        "simvastatin",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class CyclosporineHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class DiabetesHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "type",
        "insulin",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class DiureticsHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "date",
        "hydrochlorothiazide",
        "furosemide",
        "bumetanide",
        "torsemide",
        "metolazone",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class ErosionsHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class FebuxostatHypersensitivityHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "rash",
        "transaminitis",
        "cytopenia",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class FructoseHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class GoutHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "family_member",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class HeartAttackHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "number",
        "date",
        "stent",
        "cabg",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class HypertensionHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "medication",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class HyperuricemiaHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class IBDHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class LeukocytosisHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "baseline",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class LeukopeniaHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "baseline",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class OrganTransplantHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "organ",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class OsteoporosisHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class PolycythemiaHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "baseline",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class PVDHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class ShellfishHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class StrokeHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "number",
        "date",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class ThrombocytopeniaHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "baseline",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class ThrombocytosisHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "baseline",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]


class TophiHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class TransaminitisHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "baseline_alt",
        "baseline_ast",
        "last_modified",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class UrateKidneyStonesHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

class XOIInteractionsHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "value",
        "six_mp",
        "azathioprine",
        "created",
        "pk",
    )
    history_list_display = ["status"]
    search_fields = ["user__username"]

admin.site.register(Anemia, AnemiaHistoryAdmin)
admin.site.register(Angina, AnginaHistoryAdmin)
admin.site.register(AllopurinolHypersensitivity, AllopurinolHypersensitivityHistoryAdmin)
admin.site.register(CKD, CKDHistoryAdmin)
admin.site.register(Hypertension, HypertensionHistoryAdmin)
admin.site.register(Hyperuricemia, HyperuricemiaHistoryAdmin)
admin.site.register(CHF, CHFHistoryAdmin)
admin.site.register(Diabetes, DiabetesHistoryAdmin)
admin.site.register(Erosions, ErosionsHistoryAdmin)
admin.site.register(FebuxostatHypersensitivity, FebuxostatHypersensitivityHistoryAdmin)
admin.site.register(Fructose, FructoseHistoryAdmin)
admin.site.register(IBD, IBDHistoryAdmin)
admin.site.register(Leukocytosis, LeukocytosisHistoryAdmin)
admin.site.register(Leukopenia, LeukopeniaHistoryAdmin)
admin.site.register(OrganTransplant, OrganTransplantHistoryAdmin)
admin.site.register(Osteoporosis, OsteoporosisHistoryAdmin)
admin.site.register(UrateKidneyStones, UrateKidneyStonesHistoryAdmin)
admin.site.register(Diuretics, DiureticsHistoryAdmin)
admin.site.register(Cyclosporine, CyclosporineHistoryAdmin)
admin.site.register(Anticoagulation, AnticoagulationHistoryAdmin)
admin.site.register(XOIInteractions, XOIInteractionsHistoryAdmin)
admin.site.register(ColchicineInteractions, ColchicineInteractionsHistoryAdmin)
admin.site.register(Shellfish, ShellfishHistoryAdmin)
admin.site.register(Stroke, StrokeHistoryAdmin)
admin.site.register(Tophi, TophiHistoryAdmin)
admin.site.register(Thrombocytosis, ThrombocytosisHistoryAdmin)
admin.site.register(Thrombocytopenia, ThrombocytopeniaHistoryAdmin)
admin.site.register(IBD, IBDHistoryAdmin)
admin.site.register(HeartAttack, HeartAttackHistoryAdmin)
admin.site.register(Polycythemia, PolycythemiaHistoryAdmin)
admin.site.register(PVD, PVDHistoryAdmin)
admin.site.register(Bleed, BleedHistoryAdmin)
admin.site.register(Alcohol, AlcoholHistoryAdmin)
admin.site.register(Gout, GoutHistoryAdmin)
