from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from django import forms

from .models import ULTAid


class ULTAidForm(forms.ModelForm):
    class Meta:
        model = ULTAid
        fields = (
            "need",
            "want",
        )

    def __init__(self, *args, **kwargs):
        # Define self.ult from kwargs before calling super, which overwrites the kwargs
        # pop() ult from kwargs to set form self.ult to the ULT model instance passed to the ULTAidCreate view
        self.ult = kwargs.pop("ult", None)
        self.no_user = kwargs.pop("no_user", False)
        self.ckd = kwargs.pop("ckd", None)
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
                    <hr size="6" color="white" id="subfields-line">
                    """
                    ),
                    css_id="subfields",
                ),
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
        # Check if there is a ULT associated with ULTAid and hide ckd field if so, value will be set in the view
        if self.ult:
            if self.no_user == True:
                self.helper.layout[0][3].pop(1)
                self.helper.layout[0][3].pop(6)
                self.helper.layout[0][3].pop(6)
