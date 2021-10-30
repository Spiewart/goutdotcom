from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Fieldset, Layout, Submit
from django import forms

from .models import ULTAid


class ULTAidForm(forms.ModelForm):
    class Meta:
        model = ULTAid
        fields = ("ckd", "stage", "dialysis", "XOI_interactions", "organ_transplant", "allopurinol_hypersensitivity", "febuxostat_hypersensitivity", "MACE",)

    def __init__(self, *args, **kwargs):
        super(ULTAidForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.fields["ckd"].label = "CKD"
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "ckd",
                "stage",
                "dialysis",
                "XOI_interactions",
                "organ_transplant",
                "allopurinol_hypersensitivity",
                "febuxostat_hypersensitivity",
                "MACE",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
