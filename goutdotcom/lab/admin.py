from django.contrib import admin

from .models import *

# Register your models here.


class UrateAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "uric_acid",
        "created",
    )

class ALTAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "alt_sgpt",
        "created",
    )


class ASTAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ast_sgot",
        "created",
    )


class PlateletAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "platelets",
        "created",
    )


class WBCAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "white_blood_cells",
        "created",
    )


class HemoglobinAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "hemoglobin",
        "created",
    )


class CreatinineAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "creatinine",
        "eGFR_calculator",
        "created",
    )



admin.site.register(Urate, UrateAdmin)
admin.site.register(ALT, ALTAdmin)
admin.site.register(AST, ASTAdmin)
admin.site.register(Platelet, PlateletAdmin)
admin.site.register(WBC, WBCAdmin)
admin.site.register(Hemoglobin, HemoglobinAdmin)
admin.site.register(Creatinine, CreatinineAdmin)
