from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

import datetime

from .models import Height, Weight
from django import forms
from django.utils import timezone

### TO DO: ADD TESTS FOR FORMS ###

### List of years to display to users for filling date fields ###
YEARS = []

### Recursive function to populate YEARS list ###
def populate_years(x=0):
    if 1890 not in YEARS:
        current = int(datetime.date.today().year) - x
        YEARS.append(current)
        x = x+1
        populate_years(x)

### Call populate_years function ###
populate_years()


class HeightForm(forms.ModelForm):
    prefix = 'height'
    class Meta:
        model = Height
        fields = ('value', 'date_recorded',)
        error_messages = {
            'value': {
                'max_length': ("This writer's name is too long."),
            },
        }
    date_recorded = forms.DateField(widget=forms.SelectDateWidget(
        years=YEARS, empty_label=("Choose Year", "Choose Month", "Choose Day")), initial=timezone.now())

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
                'date_recorded',
            ),
        )


class WeightForm(forms.ModelForm):
    prefix = 'weight'

    class Meta:
        model = Weight
        fields = ('value', 'date_recorded',)

    date_recorded = forms.DateField(widget=forms.SelectDateWidget(
        years=YEARS, empty_label=("Choose Year", "Choose Month", "Choose Day")), initial=timezone.now())

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
                'date_recorded',
            ),
        )
