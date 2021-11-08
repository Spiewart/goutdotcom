from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from django import forms

from .models import ULT


class ULTForm(forms.ModelForm):
    uric_acid = forms.BooleanField(required=False, help_text="Is your uric acid over 9.0?")

    class Meta:
        model = ULT
        fields = ("num_flares", "freq_flares", "uric_acid")

    def __init__(self, *args, **kwargs):
        super(ULTForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

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
                        {% crispy erosions_form %}
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
                    css_id="subfields",
                ),
                "uric_acid",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
