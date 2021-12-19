from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from django import forms
from django.forms import HiddenInput

from ..ultaid.models import ULTAid
from .models import PPxAid


class PPxAidForm(forms.ModelForm):
    class Meta:
        model = PPxAid
        fields = ("perfect_health",)

    def __init__(self, *args, **kwargs):
        # Define self.flare from kwargs before calling super, which overwrites the kwargs
        # pop() flare from kwargs to set form self.flare to the Flare model instance passed to the FlareAidCreate view
        self.ultaid = kwargs.pop("ultaid", None)
        self.no_user = kwargs.pop("no_user", False)
        self.ckd = kwargs.pop("ckd", None)
        self.heartattack = kwargs.pop("heartattack", None)
        self.stroke = kwargs.pop("stroke", None)
        super(PPxAid, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                "perfect_health",
                HTML(
                    """
                    <hr size="6" color="white">
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
                    HTML(
                        """
                    <hr size="6" color="white">
                    """
                    ),
                    css_id="subfields",
                ),
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
        # Check if there is a ULTAid associated with PPxAid and hide fields passed in kwargs if so, value will be set in the view
        self.helper.layout[0][3].pop(2)
        self.helper.layout[0][3].pop(4)
        self.helper.layout[0][3].pop(6)
