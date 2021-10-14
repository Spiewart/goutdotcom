from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Field, Fieldset, Layout, Submit
from django import forms

from .models import DecisionAid, Flare


class DecisionAidForm(forms.ModelForm):
    class Meta:
        model = DecisionAid
        fields = (
            "perfect_health",
            "monoarticular",
            "ckd",
            "diabetes",
            "NSAID_contraindication",
            "osteoporosis",
            "colchicine_contraindication",
        )

    def __init__(self, *args, **kwargs):
        super(DecisionAidForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "perfect_health",
                "monoarticular",
                "ckd",
                "diabetes",
                "NSAID_contraindication",
                "osteoporosis",
                "colchicine_contraindication",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class FlareForm(forms.ModelForm):
    class Meta:
        model = Flare
        fields = (
            "location",
            "duration",
            "treatment",
            "labs",
        )

    def __init__(self, *args, **kwargs):
        super(FlareForm, self).__init__(*args, **kwargs)

        self.fields["location"].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    """
                    <input type="checkbox" id="location_check" name="location_check" value="location_check">
                    <label for="location_check">Location</label>
                    <br>
                    <input type="checkbox" id="upper_extremity_check" name="upper_extremity_check" value="upper_extremity_check">
                    <label for="upper_extremity_check">Upper Extremity</label>
                    <input type="checkbox" id="lower_extremity_check" name="lower_extremity_check" value="lower_extremity_check">
                    <label for="lower_extremity_check">Lower Extremity</label>
                    <hr id="location_check_hr" size="6" color="white">
                    """
                ),
                Div(Field("location", template="flare/widgets/location_widget.html"), id="div_id_location"),
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                "duration",
                HTML(
                    """
                    <hr size="6" color="white">
                    <input type="checkbox" id="treatment_check" name="treatment_check" value="treatment_check">
                    <label for="treatment_check">Did you treat your flare?</label>
                    """
                ),
                "treatment",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy colchicine_form %}
                    {% crispy ibuprofen_form %}
                    {% crispy naproxen_form %}
                    {% crispy celecoxib_form %}
                    {% crispy meloxicam_form %}
                    {% crispy prednisone_form %}
                    {% crispy methylprednisolone_form %}
                    {% crispy tinctureoftime_form %}
                    {% crispy othertreat_form %}
                    """
                ),
                HTML(
                    """
                    <hr size="6" color="white">
                    <input type="checkbox" id="lab_check" name="lab_check" value="lab_check">
                    <label for="lab_check">Did you get your uric acid checked during your flare?</label>
                    """
                ),
                "labs",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy urate_form %}
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
