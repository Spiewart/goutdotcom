from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from datetimewidget.widgets import DateWidget
from django import forms

from .models import (
    CHF,
    CKD,
    Alcohol,
    Anticoagulation,
    Bleed,
    BleedingEvent,
    ColchicineInteractions,
    Cyclosporine,
    Diabetes,
    Diuretics,
    Gout,
    HeartAttack,
    Hypertension,
    OrganTransplant,
    Stroke,
    UrateKidneyStones,
    XOIInteractions,
)


### Medical History ModelForms ###
class CKDForm(forms.ModelForm):
    prefix = "CKD"

    class Meta:
        model = CKD
        fields = (
            "value",
            "stage",
            "dialysis",
        )

    def __init__(self, *args, **kwargs):
        super(CKDForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("CKD", "value", "stage", "dialysis", id="CKD_for_profile"),
        )


class HypertensionForm(forms.ModelForm):
    prefix = "hypertension"

    class Meta:
        model = Hypertension
        fields = (
            "value",
            "medication",
        )

    def __init__(self, *args, **kwargs):
        super(HypertensionForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Hypertension", "value", "medication", id="hypertension_for_profile"),
        )


class CHFForm(forms.ModelForm):
    prefix = "CHF"

    class Meta:
        model = CHF
        fields = (
            "value",
            "systolic",
        )

    def __init__(self, *args, **kwargs):
        super(CHFForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("CHF", "value", "systolic", id="CHF_for_profile"),
        )


class DiabetesForm(forms.ModelForm):
    prefix = "diabetes"

    class Meta:
        model = Diabetes
        fields = (
            "value",
            "type",
            "insulin",
        )

    def __init__(self, *args, **kwargs):
        super(DiabetesForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Diabetes", "value", "type", "insulin", id="diabetes_for_profile"),
        )


class OrganTransplantForm(forms.ModelForm):
    prefix = "organ_transplant"

    class Meta:
        model = OrganTransplant
        fields = (
            "value",
            "organ",
        )

    def __init__(self, *args, **kwargs):
        super(OrganTransplantForm, self).__init__(*args, **kwargs)
        self.fields["organ"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Organ Transplant", "value", "organ", id="organ_transplant_for_profile"),
        )


class UrateKidneyStonesForm(forms.ModelForm):
    prefix = "urate_kidney_stones"

    class Meta:
        model = UrateKidneyStones
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(UrateKidneyStonesForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Diabetes", "value", id="urate_kidney_stones_for_profile"),
        )


### Contraindications ModelForms ###
class StrokeForm(forms.ModelForm):
    prefix = "stroke"

    class Meta:
        model = Stroke
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(StrokeForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Stroke", "value", id="stroke_for_contraindications"),
        )


class HeartAttackForm(forms.ModelForm):
    prefix = "heartattack"

    class Meta:
        model = HeartAttack
        fields = (
            "value",
            "stent",
            "stent_date",
            "cabg",
            "cabg_date",
        )

    def __init__(self, *args, **kwargs):
        super(HeartAttackForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Heart Attack",
                "value",
                "stent",
                "stent_date",
                "cabg",
                "cabg_date",
                id="heart_attack_for_contraindications",
            ),
        )


class BleedForm(forms.ModelForm):
    prefix = "bleed"

    class Meta:
        model = Bleed
        fields = (
            "value",
            "GIB",
            "GIB_date",
            "CNS",
            "CNS_date",
            "transfusion",
        )

    def __init__(self, *args, **kwargs):
        super(HeartAttackForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Bleed (major)",
                "value",
                "GIB",
                "GIB_date",
                "CNS",
                "CNS_date",
                "transfusion",
                id="bleed_for_contraindications",
            ),
        )
