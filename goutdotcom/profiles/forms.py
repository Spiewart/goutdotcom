import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout
from django import forms

from ..widgets.widgets import LabDurationInput
from .models import (
    FamilyProfile,
    MedicalProfile,
    PatientProfile,
    ProviderProfile,
    SocialProfile,
)


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
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
            ),
        )


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = (
            "patient_id",
            "date_of_birth",
            "gender",
            "race",
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
                "patient_id",
                "date_of_birth",
                "gender",
                "race",
            ),
        )


class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = (
            "organization",
            "titration_lab_interval",
            "monitoring_lab_interval",
            "urgent_lab_interval",
        )
        widgets = {
            "titration_lab_interval": LabDurationInput(),
            "monitoring_lab_interval": LabDurationInput(),
            "urgent_lab_interval": LabDurationInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProviderProfileForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Create your profile",
                "organization",
                "titration_lab_interval",
                "monitoring_lab_interval",
                "urgent_lab_interval",
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
