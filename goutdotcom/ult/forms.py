from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from django import forms

from .models import ULT


class ULTForm(forms.ModelForm):
    class Meta:
        model = ULT
        fields = ("num_flares", "freq_flares")

    def __init__(self, *args, **kwargs):
        super(ULTForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                "",
                "num_flares",
                HTML(
                    """
                    <hr size="6" color="white" id="num_flares-line">
                    """
                ),
                "freq_flares",
                HTML(
                    """
                    <hr size="6" color="white" id="freq_flares-line">
                    """
                ),
                Div(
                    HTML(
                        """
                    <div id="follow-up-questions">
                    <h2>Do you have any of the following?:</h2>
                    </div>
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
                        {% crispy erosions_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy hyperuricemia_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy tophi_form %}
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy urate_kidney_stones_form %}
                        """
                    ),
                    HTML(
                        """
                    <hr size="6" color="white" id="subfields-line">
                    """
                    ),
                    css_id="subfields",
                ),
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
