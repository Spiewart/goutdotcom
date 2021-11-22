from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from ..ult.urls import urlpatterns
from .models import ULTAid


class ULTAidForm(forms.ModelForm):
    ult_create_url = reverse_lazy("ult/ult:create")

    class Meta:
        model = ULTAid
        fields = (
            "need",
            "want",
        )
        help_texts = {
            "need": mark_safe("Do you need <a href=ult_create_url target='_blank'>ULT</a>?"),
        }

    def __init__(self, *args, **kwargs):
        super(ULTAidForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                "",
                "need",
                "want",
                HTML(
                    """
                    <hr size="6" color="white" id="prerequisites-line">
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
