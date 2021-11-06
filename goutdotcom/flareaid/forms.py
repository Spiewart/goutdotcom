from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from django import forms

from .models import FlareAid


class FlareAidForm(forms.ModelForm):
    class Meta:
        model = FlareAid
        fields = (
            "perfect_health",
            "monoarticular",
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # pop the 'user' from kwargs dictionary
        super(FlareAidForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                "perfect_health",
                HTML(
                    """
                    <hr size="6" color="white" id="perfect_health-line">
                    """
                ),
                "monoarticular",
                HTML(
                    """
                    <hr size="6" color="white" id="monoarticular-line">
                    """
                ),
                Div(
                    HTML(
                        """
                        <h2>Do you have a history of:</h2>
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy anticoagulation_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy bleed_form %}
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
                        {% crispy colchicine_interactions_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy diabetes_form %}
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
                        {% crispy IBD_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy osteoporosis_form %}
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
