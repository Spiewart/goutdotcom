from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Fieldset, Layout
from django import forms

from goutdotcom.flare.choices import BOOL_CHOICES

from .models import Flare


class FlareForm(forms.ModelForm):
    monoarticular = forms.TypedChoiceField(
        choices=BOOL_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == "True",
    )
    male = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    prior_gout = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    onset = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    redness = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")
    firstmtp = forms.TypedChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, coerce=lambda x: x == "True")

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
            "duration",
            "treatment",
        )

    def __init__(self, *args, **kwargs):
        super(FlareForm, self).__init__(*args, **kwargs)
        self.fields["firstmtp"].label = "Was the flare in the base of the big toe?"
        self.fields["location"].label = "Joints involved"
        self.fields["monoarticular"].label = "Was it only in one joint?"
        self.fields["male"].label = "Sex: are you male (biologically)?"
        self.fields["onset"].label = "Rapid onset: did the symptoms start and reach maximum intensity in a day or less?"
        self.fields["prior_gout"].label = "Gout history: have you had gout or symptoms suggestive of gout before?"
        self.fields["redness"].label = "Erythema (redness): as the skin above the affected joint red and angry looking?"
        self.fields["treatment"].label = "Did you treat your gout flare with anything?"

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    """
                    <h2>Location</h2>
                    """
                ),
                "monoarticular",
                "firstmtp",
                InlineCheckboxes("location"),
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                HTML(
                    """
                    <h2>Symptoms</h2>
                    """
                ),
                "onset",
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
                "redness",
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                HTML(
                    """
                    <h2>History</h2>
                    """
                ),
                "male",
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
                Div(
                    HTML(
                        """
                        <span>Do you have any cardiac disease(s) or equivalents?</span>
                        """
                    ),
                    css_id="cardiacdiseases",
                ),
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy angina_form %}
                    {% crispy hypertension_form %}
                    {% crispy heartattack_form %}
                    {% crispy CHF_form %}
                    {% crispy stroke_form %}
                    {% crispy PVD_form %}
                    """
                ),
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                HTML(
                    """
                    <h2>Treatment</h2>
                    """
                ),
                InlineCheckboxes("treatment"),
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
            ),
        )
