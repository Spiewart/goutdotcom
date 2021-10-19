from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Fieldset, Layout, Submit
from django import forms

from .choices import BOOL_CHOICES, FREQ_CHOICES, ULT_CHOICES
from .models import ULT


class ULTForm(forms.ModelForm):
    erosions = forms.BooleanField(required=False, help_text="Do you have erosions on x-rays or other imaging?")
    tophi = forms.BooleanField(required=False, help_text="Do you have gouty tophi?")
    stones = forms.BooleanField(required=False, help_text="Do you get uric acid kidney stones?")
    ckd = forms.BooleanField(required=False, help_text="Do you have chronic kidney disease (CKD)?")
    uric_acid = forms.BooleanField(required=False, help_text="Is your uric acid over 9.0?")

    class Meta:
        model = ULT
        fields = ("num_flares", "freq_flares", "erosions", "tophi", "stones", "ckd", "uric_acid")

    def __init__(self, *args, **kwargs):
        super(ULTForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.fields["ckd"].label = "CKD"
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "num_flares",
                "freq_flares",
                HTML(
                    """
                    <div id="follow-up-questions">
                    <hr size="6" color="white">
                    <h3>Do you have any of the following?:</h3>
                    </div>
                    """
                ),
                "erosions",
                "tophi",
                "stones",
                "ckd",
                "uric_acid",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
