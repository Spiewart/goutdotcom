from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Fieldset, Layout
from django import forms
from django.utils.safestring import mark_safe

from goutdotcom.flare.choices import BOOL_CHOICES

from .models import Flare


class FlareForm(forms.ModelForm):
    monoarticular = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    male = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    prior_gout = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    onset = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    redness = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    firstmtp = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    cardiacdisease = forms.TypedChoiceField(
        choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True"
    )

    class Meta:
        model = Flare
        fields = (
            "monoarticular",
            "male",
            "prior_gout",
            "onset",
            "redness",
            "firstmtp",
            "location",
            "cardiacdisease",
            "duration",
            "treatment",
        )

    def __init__(self, *args, **kwargs):
        super(FlareForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "monoarticular",
                "firstmtp",
                InlineCheckboxes("location"),
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                "duration",
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                "male",
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                "onset",
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                "prior_gout",
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                "redness",
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                InlineCheckboxes("treatment"),
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy urate_form %}
                    """
                ),
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                "cardiacdisease",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy hypertension_form %}
                    {% crispy heartattack_form %}
                    {% crispy CHF_form %}
                    {% crispy stroke_form %}
                    {% crispy PVD_form %}
                    <br>
                    """
                ),
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
            ),
        )
