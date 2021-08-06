from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

import datetime

from .models import Height, Weight
from django import forms
from django.utils import timezone

### TO DO: ADD TESTS FOR FORMS ###

class HeightForm(forms.ModelForm):
    prefix = 'height'

    class Meta:
        model = Height
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(HeightForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Height in inches',
                'value',
            ),
        )
        self.fields['value'].label = "Height"


class WeightForm(forms.ModelForm):
    prefix = 'weight'

    class Meta:
        model = Weight
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(WeightForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Weight in pounds',
                'value',
            ),
        )
        self.fields['value'].label = "Weight"
