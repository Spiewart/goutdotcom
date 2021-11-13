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
                "freq_flares",
                HTML(
                    """
                    <hr size="6" color="white">
                    """
                ),
                Div(
                    HTML(
                        """
                    <div id="follow-up-questions">
                    <h3>Do you have any of the following?:</h3>
                    </div>
                    """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy CKD_form %}
                        <hr size="6" color="white">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy erosions_form %}
                        <hr size="6" color="white">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy hyperuricemia_form %}
                        <hr size="6" color="white">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy tophi_form %}
                        <hr size="6" color="white">
                        """
                    ),
                    HTML(
                        """
                        {% load crispy_forms_tags %}
                        {% crispy urate_kidney_stones_form %}
                        <hr size="6" color="white">
                        """
                    ),
                    css_id="subfields",
                ),
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
