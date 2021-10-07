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
    ColchicineInteractions,
    Cyclosporine,
    Diabetes,
    Diuretics,
    Erosions,
    Fructose,
    Gout,
    HeartAttack,
    Hypertension,
    OrganTransplant,
    Shellfish,
    Stroke,
    Tophi,
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


class ErosionsForm(forms.ModelForm):
    prefix = "erosions"

    class Meta:
        model = Erosions
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ErosionsForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Erosions", "value", id="erosions_for_profile"),
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


class TophiForm(forms.ModelForm):
    prefix = "tophi"

    class Meta:
        model = Tophi
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(TophiForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Tophi", "value", id="tophi_for_profile"),
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
        fields = (
            "value",
            "number",
            "date",
        )
        widgets = {
            # Use localization and bootstrap 3
            "date": DateWidget(attrs={"id": "stroke_date.pk"}, usel10n=True, bootstrap_version=3),
        }

    def __init__(self, *args, **kwargs):
        super(StrokeForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Stroke", "value", "number", "date", id="stroke_for_contraindications"),
        )


class HeartAttackForm(forms.ModelForm):
    prefix = "heartattack"

    class Meta:
        model = HeartAttack
        fields = (
            "value",
            "number",
            "date",
            "stent",
            "stent_date",
            "cabg",
            "cabg_date",
        )
        dateTimeOptions = {
            "autoclose": True,
            "pickerPosition": "bottom-left",
        }
        widgets = {
            # Use localization and bootstrap 3
            "date": DateWidget(attrs={"id": "heartattack_date.pk"}, usel10n=True, bootstrap_version=3),
            "stent_date": DateWidget(attrs={"id": "stent_date.pk"}, usel10n=True, bootstrap_version=3),
            "cabg_date": DateWidget(attrs={"id": "cabg_date.pk"}, usel10n=True, bootstrap_version=3),
        }

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
                "number",
                "date",
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
            "number",
            "date",
            "GIB",
            "GIB_date",
            "CNS",
            "CNS_date",
            "transfusion",
        )
        dateTimeOptions = {
            "autoclose": True,
            "pickerPosition": "bottom-left",
        }
        widgets = {
            # Use localization and bootstrap 3
            "date": DateWidget(
                options=dateTimeOptions, attrs={"id": "bleed_date.pk"}, usel10n=True, bootstrap_version=3
            ),
            "GIB_date": DateWidget(
                options=dateTimeOptions, attrs={"id": "GIB_date.pk"}, usel10n=True, bootstrap_version=3
            ),
            "CNS_date": DateWidget(
                options=dateTimeOptions, attrs={"id": "CNS_date.pk"}, usel10n=True, bootstrap_version=3
            ),
        }

    def __init__(self, *args, **kwargs):
        super(BleedForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Bleed (major)",
                "value",
                "number",
                "date",
                "GIB",
                "GIB_date",
                "CNS",
                "CNS_date",
                "transfusion",
                id="bleed_for_contraindications",
            ),
        )


### Family History Forms ###


class GoutForm(forms.ModelForm):
    prefix = "gout"

    class Meta:
        model = Gout
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(GoutForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Gout", "value", id="gout_for_profile"),
        )


### Social History Forms ###
class AlcoholForm(forms.ModelForm):
    prefix = "alcohol"

    class Meta:
        model = Alcohol
        fields = (
            "value",
            "number",
            "wine",
            "beer",
            "liquor",
        )

    def __init__(self, *args, **kwargs):
        super(AlcoholForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Alcohol", "value", "number", "wine", "beer", "liquor", id="alcohol_for_profile"),
        )


class FructoseForm(forms.ModelForm):
    prefix = "fructose"

    class Meta:
        model = Fructose
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(FructoseForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Fructose", "value", id="fructose_for_profile"),
        )


class ShellfishForm(forms.ModelForm):
    prefix = "shellfish"

    class Meta:
        model = Shellfish
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ShellfishForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("Shellfish", "value", id="shellfish_for_profile"),
        )
