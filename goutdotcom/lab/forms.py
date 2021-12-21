from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Fieldset, Layout, Submit
from datetimewidget.widgets import DateTimeWidget
from django import forms

from .models import Urate

class ULTPlanForm(forms.ModelForm):
    pass

class UrateForm(forms.ModelForm):
    class Meta:
        model = Urate
        fields = (
            "value",
            "date_drawn",
        )
        dateTimeOptions = {
            "autoclose": True,
            "pickerPosition": "bottom-left",
        }
        widgets = {
            # Use localization and bootstrap 3
            "date_drawn": DateTimeWidget(
                options=dateTimeOptions, attrs={"id": "urate-date_drawn.pk"}, usel10n=True, bootstrap_version=3
            )
        }

    def __init__(self, *args, **kwargs):
        super(UrateForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a uric acid",
                "value",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class UrateFlareForm(UrateForm):
    prefix = "urate"

    class Meta:
        model = Urate
        fields = ("value",)
        widgets = {
            "value": forms.NumberInput(attrs={"step": 0.10}),
        }

    def __init__(self, *args, **kwargs):
        super(UrateFlareForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = "Do you know what your uric acid was during your flare?"
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                id="urate_fields",
            ),
        )
