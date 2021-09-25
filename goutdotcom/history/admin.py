from django.contrib import admin

from .models import *

# Register your models here.


class CKDAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "stage",
        "dialysis",
        "created",
        "pk",
    )


class HypertensionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "medication",
        "created",
        "pk",
    )


class CHFAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "systolic",
        "created",
        "pk",
    )


class DiabetesAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "type",
        "insulin",
        "created",
        "pk",
    )


class OrganTransplantAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "organ",
        "created",
        "pk",
    )


class UrateKidneyStonesAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )


class DiureticsAdmin(admin.ModelAdmin):
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


class CyclosporineAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "date",
        "created",
        "pk",
    )


class AnticoagulationAdmin(admin.ModelAdmin):
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


class XOIInteractionsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "six_mp",
        "azathioprine",
        "created",
        "pk",
    )


class ColchicineInteractionsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "clarithromycin",
        "simvastatin",
        "created",
        "pk",
    )


class StrokeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "number",
        "date",
        "created",
        "pk",
    )


class HeartAttackAdmin(admin.ModelAdmin):
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


class BleedAdmin(admin.ModelAdmin):
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


class AlcoholAdmin(admin.ModelAdmin):
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


class FructoseAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )


class ShellfishAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "created",
        "pk",
    )


class GoutAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "family_member",
        "created",
        "pk",
    )


admin.site.register(CKD, CKDAdmin)
admin.site.register(Hypertension, HypertensionAdmin)
admin.site.register(CHF, CHFAdmin)
admin.site.register(Diabetes, DiabetesAdmin)
admin.site.register(Fructose, FructoseAdmin)
admin.site.register(OrganTransplant, OrganTransplantAdmin)
admin.site.register(UrateKidneyStones, UrateKidneyStonesAdmin)
admin.site.register(Diuretics, DiureticsAdmin)
admin.site.register(Cyclosporine, CyclosporineAdmin)
admin.site.register(Anticoagulation, AnticoagulationAdmin)
admin.site.register(XOIInteractions, XOIInteractionsAdmin)
admin.site.register(ColchicineInteractions, ColchicineInteractionsAdmin)
admin.site.register(Shellfish, ShellfishAdmin)
admin.site.register(Stroke, StrokeAdmin)
admin.site.register(HeartAttack, HeartAttackAdmin)
admin.site.register(Bleed, BleedAdmin)
admin.site.register(Alcohol, AlcoholAdmin)
admin.site.register(Gout, GoutAdmin)
