from django.contrib import admin

from .models import *

# Register your models here.


class UrateAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )

class ALTAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )


class ASTAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )


class PlateletAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )


class WBCAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )


class HemoglobinAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "date_drawn",
        "created",
    )


class CreatinineAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "value",
        "eGFR_calculator",
        "date_drawn",
        "created",
    )



admin.site.register(Urate, UrateAdmin)
admin.site.register(ALT, ALTAdmin)
admin.site.register(AST, ASTAdmin)
admin.site.register(Platelet, PlateletAdmin)
admin.site.register(WBC, WBCAdmin)
admin.site.register(Hemoglobin, HemoglobinAdmin)
admin.site.register(Creatinine, CreatinineAdmin)
