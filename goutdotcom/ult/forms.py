from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django import forms

from .models import ULT


class ULTForm(forms.ModelForm):
    class Meta:
        model = ULT
        fields = ("num_flares", "freq_flares", "uric_acid")

    def __init__(self, *args, **kwargs):
        super(ULTForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "num_flares",
                "freq_flares",
                "uric_acid",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
