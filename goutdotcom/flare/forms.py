from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Fieldset, Layout
from django import forms
from django.forms import HiddenInput

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
        self.gender = kwargs.pop("gender", None)
        super(FlareForm, self).__init__(*args, **kwargs)
        self.fields["firstmtp"].label = "Was it in the big toe?"
        self.fields["location"].label = "Joints involved"
        self.fields["location"].help_text = None
        self.fields["monoarticular"].label = "Only one joint?"
        self.fields["male"].label = "Male (biologically)?"
        self.fields["onset"].label = "Symptoms start and peak in a day or less?"
        self.fields["prior_gout"].label = "Had gout before?"
        self.fields["redness"].label = "Is the skin around the painful joint(s) red?"
        self.fields["treatment"].label = "Take anything for the symptoms?"

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    HTML(
                        """
                        <hr size="6" color="dark">
                        """
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                <legend>Location</legend>
                                """
                            ),
                            css_class="col-auto",
                        ),
                        css_id="row",
                    ),
                    Div(
                        Div(
                            "monoarticular",
                            css_class="col-auto",
                        ),
                        Div(
                            "firstmtp",
                            css_class="col-auto",
                        ),
                        Div(
                            InlineCheckboxes("location"),
                            css_class="col",
                        ),
                        css_class="row",
                    ),
                    HTML(
                        """
                        <hr size="6" color="dark">
                        """
                    ),
                    css_id="location",
                ),
                Div(
                    Div(
                        Div(
                            HTML(
                                """
                                <legend>Symptoms</legend>
                                """
                            ),
                            css_class="col-auto",
                        ),
                        css_id="row",
                    ),
                    Div(
                        Div(
                            "onset",
                            css_class="col",
                        ),
                        Div(
                            "ongoing",
                            css_class="col",
                        ),
                        Div(
                            "duration",
                            css_class="col",
                        ),
                        Div(
                            "redness",
                            css_class="col",
                        ),
                        css_class="row",
                    ),
                    HTML(
                        """
                            <hr size="6" color="dark">
                            """
                    ),
                    css_id="symptoms",
                ),
                Div(
                    Div(
                        Div(
                            HTML(
                                """
                                <legend>History</legend>
                                """
                            ),
                            css_class="col-auto",
                        ),
                        css_id="row",
                    ),
                    Div(
                        Div(
                            "male",
                            css_class="col",
                        ),
                        Div(
                            "prior_gout",
                            css_class="col",
                        ),
                        Div(
                            HTML(
                                """
                                {% load crispy_forms_tags %}
                                {% crispy urate_form %}
                                """
                            ),
                            css_class="col",
                        ),
                        css_class="row",
                    ),
                    HTML(
                        """
                        <hr size="6" color="dark">
                        """
                    ),
                    css_id="history",
                ),
                Div(
                    Div(
                        Div(
                            HTML(
                                """
                                <legend>Cardiovascular Disease</legend>
                                """
                            ),
                            css_class="col-auto",
                        ),
                        css_id="row",
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                {% load crispy_forms_tags %}
                                {% crispy angina_form %}
                                """
                            ),
                            css_class="col",
                        ),
                        Div(
                            HTML(
                                """
                                {% load crispy_forms_tags %}
                                {% crispy hypertension_form %}
                                """
                            ),
                            css_class="col",
                        ),
                        Div(
                            HTML(
                                """
                                {% load crispy_forms_tags %}
                                {% crispy heartattack_form %}
                                """
                            ),
                            css_class="col",
                        ),
                        Div(
                            HTML(
                                """
                                {% load crispy_forms_tags %}
                                {% crispy CHF_form %}
                                """
                            ),
                            css_class="col",
                        ),
                        Div(
                            HTML(
                                """
                                {% load crispy_forms_tags %}
                                {% crispy stroke_form %}
                                """
                            ),
                            css_class="col",
                        ),
                        Div(
                            HTML(
                                """
                                {% load crispy_forms_tags %}
                                {% crispy PVD_form %}
                                """
                            ),
                            css_class="col",
                        ),
                        css_class="row",
                    ),
                    HTML(
                        """
                        <hr size="6" color="dark">
                        """
                    ),
                    css_id="cardiacdiseases",
                ),
                Div(
                    Div(
                        Div(
                            HTML(
                                """
                                <legend>Treatment</legend>
                                """
                            ),
                            css_class="col-auto",
                        ),
                        css_id="row",
                    ),
                    Div(
                        Div(
                            InlineCheckboxes("treatment"),
                            css_class="col",
                        ),
                        css_class="row",
                    ),
                    HTML(
                        """
                        <hr size="6" color="dark">
                        """
                    ),
                    css_id="treatment",
                ),
            ),
        )
        # Check if there is a gender associated with Flare (and creating User's profile) and hide male field if so, value will be set in the view
        # Set initial value to False so as to avoid leaving required field blank
        # Also have to remove dark line for style by layout[index]
        if self.gender:
            self.fields["male"].widget = HiddenInput()
            self.initial["male"] = False
            self.helper.layout[0].pop(14)
