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
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    HTML(
                        """
                        <h2>Do you have a history of:</h2>
                    """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy CKD_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy XOI_interactions_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy organ_transplant_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy allopurinol_hypersensitivity_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy febuxostat_hypersensitivity_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy heartattack_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy stroke_form %}
                        """
                    ),
                    css_id="subfields",
                ),
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
