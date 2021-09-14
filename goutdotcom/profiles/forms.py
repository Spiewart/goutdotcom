import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout
from datetimewidget.widgets import DateWidget
from django import forms

from .models import MedicalProfile, PatientProfile

YEARS = []


def populate_years(x=0):
    if 1890 not in YEARS:
        current = int(datetime.date.today().year) - x
        YEARS.append(current)
        x = x + 1
        populate_years(x)


populate_years()


class MedicalProfileForm(forms.ModelForm):
    class Meta:
        model = MedicalProfile
        fields = ()

    def __init__(self, *args, **kwargs):
        super(MedicalProfileForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log your medical history",
            ),
        )


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = (
            "picture",
            "bio",
            "date_of_birth",
            "gender",
            "race",
        )
        widgets = {
            # Use localization and bootstrap 3
            "date_of_birth": DateWidget(attrs={"id": "date_of_birth"}, usel10n=True, bootstrap_version=3),
        }

    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=YEARS, empty_label=("Choose Year", "Choose Month", "Choose Day"))
    )

    def __init__(self, *args, **kwargs):
        super(PatientProfileForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Create your profile",
                "picture",
                "date_of_birth",
                "gender",
                "race",
            ),
        )
