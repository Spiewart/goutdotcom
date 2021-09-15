from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from datetimewidget.widgets import DateWidget

from django import forms

from .models import CKD, Hypertension, CHF, Diabetes, OrganTransplant, UrateKidneyStones, Diuretics, Cyclosporine, Anticoagulation, XOIInteractions, ColchicineInteractions, Stroke, HeartAttack, BleedingEvent, Alcohol, Gout

class CKDForm(forms.ModelForm):
    prefix = 'CKD'

    class Meta:
        model = CKD
        fields = ('value', 'stage', 'dialysis',)

    def __init__(self, *args, **kwargs):
        super(CKDForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'CKD',
                'value',
                'stage',
                'dialysis',
                id='CKD_for_profile'
            ),
        )


class HypertensionForm(forms.ModelForm):
    prefix = 'hypertension'

    class Meta:
        model = Hypertension
        fields = ('value', 'medication',)

    def __init__(self, *args, **kwargs):
        super(HypertensionForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Hypertension',
                'value',
                'medication',
                id='hypertension_for_profile'
            ),
        )


class CHFForm(forms.ModelForm):
    prefix = 'CHF'

    class Meta:
        model = CHF
        fields = ('value', 'systolic',)

    def __init__(self, *args, **kwargs):
        super(CHFForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'CHF',
                'value',
                'systolic',
                id='CHF_for_profile'
            ),
        )


class DiabetesForm(forms.ModelForm):
    prefix = 'diabetes'

    class Meta:
        model = Diabetes
        fields = ('value', 'type', 'insulin',)

    def __init__(self, *args, **kwargs):
        super(DiabetesForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Diabetes',
                'value',
                'type',
                'insulin',
                id='diabetes_for_profile'
            ),
        )


class OrganTransplantForm(forms.ModelForm):
    prefix = 'organ_transplant'

    class Meta:
        model = OrganTransplant
        fields = ('value', 'organ',)

    def __init__(self, *args, **kwargs):
        super(OrganTransplantForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Diabetes',
                'value',
                'organ',
                id='organ_transplant_for_profile'
            ),
        )


class UrateKidneyStonesForm(forms.ModelForm):
    prefix = 'urate_kidney_stones'

    class Meta:
        model = UrateKidneyStones
        fields = ('value',)

    def __init__(self, *args, **kwargs):
        super(UrateKidneyStonesForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Diabetes',
                'value',
                id='urate_kidney_stones_for_profile'
            ),
        )
