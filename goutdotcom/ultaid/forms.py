from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from django import forms

from .models import ULTAid


class ULTAidForm(forms.ModelForm):
    class Meta:
        model = ULTAid
        fields = ()

    def __init__(self, *args, **kwargs):
        super(ULTAidForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    HTML(
                        """
                        <h2>Do you have a history of:</h2>
                        <hr size="6" color="white" id="monoarticular-line">
                    """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy CKD_form %}
                        <hr size="6" color="white" id="monoarticular-line">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy XOI_interactions_form %}
                        <hr size="6" color="white" id="monoarticular-line">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy organ_transplant_form %}
                        <hr size="6" color="white" id="monoarticular-line">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy allopurinol_hypersensitivity_form %}
                        <hr size="6" color="white" id="monoarticular-line">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy febuxostat_hypersensitivity_form %}
                        <hr size="6" color="white" id="monoarticular-line">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy heartattack_form %}
                        <hr size="6" color="white" id="monoarticular-line">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy stroke_form %}
                        <hr size="6" color="white" id="monoarticular-line">
                        """
                    ),
                    css_id="subfields",
                ),
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
