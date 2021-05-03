from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit


from .models import Urate
from django import forms

class UrateForm(forms.ModelForm):
    class Meta:
        model = Urate
        fields = ('uric_acid',)

    FormHelper.form_tag = False

    def __init__(self, *args, **kwargs):
        super(UrateForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log your flare',
                'uric_acid', 
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )