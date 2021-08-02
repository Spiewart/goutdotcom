from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit
from dateutil.relativedelta import relativedelta
import datetime

from .models import PatientProfile
from django import forms

YEARS = []

def populate_years(x=0):
    if 1890 not in YEARS:
        current = int(datetime.date.today().year) - x
        YEARS.append(current)
        x = x+1
        populate_years(x)

populate_years()

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ('picture', 'bio', 'date_of_birth', 'gender', 'race',)

    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS, empty_label=("Choose Year", "Choose Month", "Choose Day")))

    def __init__(self, *args, **kwargs):
        super(PatientProfileForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Create your profile',
                'picture',
                'date_of_birth',
                'gender',
                'race',
                ),
        )
