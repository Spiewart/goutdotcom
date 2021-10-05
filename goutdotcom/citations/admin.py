from django.contrib import admin
from django.shortcuts import render
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.urls import path

from .forms import BibtexUploadForm
from .models import Reference


class ReferenceAdmin(admin.ModelAdmin):
    change_list_template = "citations/admin/updated_change_form.html"

    def get_urls(self):
        urls = super(ReferenceAdmin, self).get_urls()

        # if "BibtexUploadForm" in globals():
        new_urls = [
            path(
                "upload_bibtex/",
                view=self.admin_site.admin_view(self.upload_bibtex_view),
                name="citations_reference_upload_bibtex",
            )
        ]
        return new_urls + urls

        # else:
        # return urls

    def upload_bibtex_view(self, request):
        # if not "BibtexUploadForm" in globals():
        # return render("admin/unable_to_upload_bibtex.html", {})

        # else:
        if request.method == "POST":
            form = BibtexUploadForm(request.POST, request.FILES)
            if form.is_valid():
                records = form.save()
                context = {"form": form, "success": True, "records": records}
                return TemplateResponse(request, "citations/admin/imported.html", context)
        else:
            form = BibtexUploadForm()
            context = {"form": form}
            return TemplateResponse(request, "citations/admin/imported.html", context)


admin.site.register(Reference, ReferenceAdmin)