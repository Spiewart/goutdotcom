import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout
from datetimewidget.widgets import DateWidget
from django import forms

from .models import FamilyProfile, MedicalProfile, PatientProfile, SocialProfile


class FamilyProfileForm(forms.ModelForm):
    class Meta:
        model = FamilyProfile
        fields = ()

    def __init__(self, *args, **kwargs):
        super(FamilyProfileForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log your family history",
            ),
        )


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
        dateTimeOptions = {
            "autoclose": True,
            "pickerPosition": "bottom-left",
        }
        widgets = {
            # Use localization and bootstrap 3
            "date_of_birth": DateWidget(
                options=dateTimeOptions, attrs={"id": "date_of_birth.pk"}, usel10n=True, bootstrap_version=3
            )
        }

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


class SocialProfileForm(forms.ModelForm):
    class Meta:
        model = SocialProfile
        fields = ()

    def __init__(self, *args, **kwargs):
        super(SocialProfileForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log your social / dietary history",
            ),
        )
