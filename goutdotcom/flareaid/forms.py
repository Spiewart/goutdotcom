from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Fieldset, Layout, Submit
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
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy CKD_form %}
                    """
                ),
                HTML(
                    """
                    <hr size="6" color="white" id="ckd-line">
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
                    <hr size="6" color="white" id="colchicine_interactions-line">
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
                    <hr size="6" color="white" id="colchicine_interactions-line">
                    """
                ),
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
