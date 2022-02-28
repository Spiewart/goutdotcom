from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from datetimewidget.widgets import DateWidget
from django import forms

from .models import (
    CHF,
    CKD,
    IBD,
    PVD,
    Alcohol,
    AllopurinolHypersensitivity,
    Anemia,
    Angina,
    Anticoagulation,
    Bleed,
    ColchicineInteractions,
    Cyclosporine,
    Diabetes,
    Diuretics,
    Erosions,
    FebuxostatHypersensitivity,
    Fructose,
    Gout,
    HeartAttack,
    Hypertension,
    Hyperuricemia,
    Leukocytosis,
    Leukopenia,
    OrganTransplant,
    Osteoporosis,
    Polycythemia,
    Shellfish,
    Stroke,
    Thrombocytopenia,
    Thrombocytosis,
    Tophi,
    Transaminitis,
    UrateKidneyStones,
    XOIInteractions,
)


### Medical History ModelForms ###
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
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Alcohol", "value", "number", "wine", "beer", "liquor", id="alcohol_for_profile"),
        )


class AllopurinolHypersensitivityForm(forms.ModelForm):
    prefix = "AllopruinolHypersensitivity"

    class Meta:
        model = AllopurinolHypersensitivity
        fields = (
            "value",
            "rash",
            "transaminitis",
            "cytopenia",
        )

    def __init__(self, *args, **kwargs):
        super(AllopurinolHypersensitivityForm, self).__init__(*args, **kwargs)
        self.fields["value"].label = "Allopurinol Side Effects"
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Allopurinol Hypersensitivity",
                "value",
                "rash",
                "transaminitis",
                "cytopenia",
                id="allopurinolhypersensitivity_for_profile",
            ),
        )


class AllopurinolHypersensitivitySimpleForm(AllopurinolHypersensitivityForm):
    class Meta:
        model = AllopurinolHypersensitivity
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(AllopurinolHypersensitivityForm, self).__init__(*args, **kwargs)
        self.fields["value"].label = "Allopurinol Side Effects"
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="gout_for_profile"),
        )


class AnemiaForm(forms.ModelForm):
    prefix = "anemia"

    class Meta:
        model = Anemia
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(AnemiaForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy hemoglobin_anemia_form %}
                    """
                ),
                id="anemia_for_profile",
            ),
        )


class AnginaForm(forms.ModelForm):
    prefix = "Angina"

    class Meta:
        model = Angina
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(AnginaForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                id="angina_for_profile",
            ),
        )


class AnticoagulationForm(forms.ModelForm):
    prefix = "Anticoagulation"

    class Meta:
        model = Anticoagulation
        fields = (
            "value",
            "apixaban",
            "clopidogrel",
            "dabigatran",
            "enoxaparin",
            "rivaroxaban",
            "warfarin",
        )

    def __init__(self, *args, **kwargs):
        super(AnticoagulationForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                "Anticoagulation",
                "value",
                "apixaban",
                "clopidogrel",
                "dabigatran",
                "enoxaparin",
                "rivaroxaban",
                "warfarin",
                id="anticoagulation_for_profile",
            ),
        )


class AnticoagulationSimpleForm(AnticoagulationForm):
    class Meta:
        model = Anticoagulation
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(AnticoagulationSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                id="anticoagulation_for_profile",
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
        self.helper = FormHelper(self)
        self.helper.form_tag = False
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
                id="bleed_for_profile",
            ),
        )


class BleedSimpleForm(BleedForm):
    class Meta:
        model = Bleed
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(BleedSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                id="bleed_for_contraindications",
            ),
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
        self.fields["value"].widget = forms.CheckboxInput()
        self.fields["systolic"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("", "value", "systolic", id="CHF_for_profile"),
        )


class CHFSimpleForm(CHFForm):
    class Meta:
        model = CHF
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(CHFForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("", "value", id="CHF_for_profile"),
        )


class CKDSimpleForm(forms.ModelForm):
    prefix = "CKD"

    class Meta:
        model = CKD
        fields = (
            "value",
            "dialysis",
        )

    def __init__(self, *args, **kwargs):
        super(CKDSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.fields["dialysis"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                "dialysis",
                id="CKD_for_profile",
            ),
        )


class CKDForm(CKDSimpleForm):
    class Meta:
        model = CKD
        fields = (
            "value",
            "dialysis",
            "stage",
        )

    def __init__(self, *args, **kwargs):
        super(CKDForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.fields["dialysis"].widget = forms.CheckboxInput()
        self.fields["stage"].empty_label = None
        self.fields["stage"].required = False
        self.fields["stage"].widget = forms.RadioSelect()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                "dialysis",
                InlineCheckboxes("stage"),
                id="CKD_for_profile",
            ),
        )


class ColchicineInteractionsForm(forms.ModelForm):
    prefix = "ColchicineInteractions"

    class Meta:
        model = ColchicineInteractions
        fields = (
            "value",
            "clarithromycin",
            "simvastatin",
        )

    def __init__(self, *args, **kwargs):
        super(ColchicineInteractionsForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Colchicine Interactions",
                "value",
                "clarithromycin",
                "simvastatin",
                id="colchicine_interactions_for_profile",
            ),
        )


class ColchicineInteractionsSimpleForm(ColchicineInteractionsForm):
    class Meta:
        model = ColchicineInteractions
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ColchicineInteractionsSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                id="colchicine_interactions_for_profile",
            ),
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
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Diabetes", "value", "type", "insulin", id="diabetes_for_profile"),
        )


class DiabetesSimpleForm(DiabetesForm):
    class Meta:
        model = Diabetes
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(DiabetesSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="diabetes_for_profile"),
        )


class ErosionsForm(forms.ModelForm):
    prefix = "erosions"

    class Meta:
        model = Erosions
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ErosionsForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="erosions_for_profile"),
        )


class FebuxostatHypersensitivityForm(forms.ModelForm):
    prefix = "FebuxostatHypersensitivity"

    class Meta:
        model = FebuxostatHypersensitivity
        fields = (
            "value",
            "rash",
            "transaminitis",
            "cytopenia",
        )

    def __init__(self, *args, **kwargs):
        super(FebuxostatHypersensitivityForm, self).__init__(*args, **kwargs)
        self.fields["value"].label = "Febuxostat Side Effects"
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Febuxostat Hypersensitivity",
                "value",
                "rash",
                "transaminitis",
                "cytopenia",
                id="febuxostathypersensitivity_for_profile",
            ),
        )


class FebuxostatHypersensitivitySimpleForm(FebuxostatHypersensitivityForm):
    class Meta:
        model = FebuxostatHypersensitivity
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(FebuxostatHypersensitivityForm, self).__init__(*args, **kwargs)
        self.fields["value"].label = "Febuxostat Side Effects"
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="febuxostathypersensitivity_for_profile"),
        )


class FructoseForm(forms.ModelForm):
    prefix = "fructose"

    class Meta:
        model = Fructose
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(FructoseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Fructose", "value", id="fructose_for_profile"),
        )


class GoutForm(forms.ModelForm):
    prefix = "gout"

    class Meta:
        model = Gout
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(GoutForm, self).__init__(*args, **kwargs)
        self.fields["value"].label = "Gout Family History"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Gout", "value", id="gout_for_profile"),
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
            "date": DateWidget(attrs={"id": "heartattack_date.pk"}, usel10n=True, bootstrap_version=3),
            "stent_date": DateWidget(attrs={"id": "stent_date.pk"}, usel10n=True, bootstrap_version=3),
            "cabg_date": DateWidget(attrs={"id": "cabg_date.pk"}, usel10n=True, bootstrap_version=3),
        }

    def __init__(self, *args, **kwargs):
        super(HeartAttackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
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


class HeartAttackSimpleForm(HeartAttackForm):
    class Meta:
        model = HeartAttack
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(HeartAttackSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                id="heart_attack_for_contraindications",
            ),
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
        self.fields["value"].widget = forms.CheckboxInput()
        self.fields["medication"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("", "value", "medication", id="hypertension_for_profile"),
        )


class HypertensionSimpleForm(HypertensionForm):
    class Meta:
        model = Hypertension
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(HypertensionForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("", "value", id="hypertension_for_profile"),
        )


class HyperuricemiaForm(forms.ModelForm):
    prefix = "hyperuricemia"

    class Meta:
        model = Hyperuricemia
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(HyperuricemiaForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="hyperuricemia_for_profile"),
        )


class IBDForm(forms.ModelForm):
    prefix = "IBD"

    class Meta:
        model = IBD
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(IBDForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Inflammatory Bowel Disease", "value", id="IBD_for_profile"),
        )


class IBDSimpleForm(IBDForm):
    def __init__(self, *args, **kwargs):
        super(IBDSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="IBD_for_profile"),
        )


class LeukocytosisForm(forms.ModelForm):
    prefix = "leukocytosis"

    class Meta:
        model = Leukocytosis
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(LeukocytosisForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy wbc_leukocytosis_form %}
                    """
                ),
                id="leukocytosis_for_profile",
            ),
        )


class LeukopeniaForm(forms.ModelForm):
    prefix = "leukopenia"

    class Meta:
        model = Leukopenia
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(LeukopeniaForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy wbc_leukopenia_form %}
                    """
                ),
                id="leukopenia_for_profile",
            ),
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
        self.fields["value"].widget = forms.CheckboxInput()
        self.fields["organ"].required = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", InlineCheckboxes("organ"), id="organ_transplant_for_profile"),
        )


class OsteoporosisForm(forms.ModelForm):
    prefix = "Osteoporosis"

    class Meta:
        model = Osteoporosis
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(OsteoporosisForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Osteoporosis", "value", id="osteoporosis_for_profile"),
        )


class OsteoporosisSimpleForm(OsteoporosisForm):
    def __init__(self, *args, **kwargs):
        super(OsteoporosisSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="osteoporosis_for_profile"),
        )


class PolycythemiaForm(forms.ModelForm):
    prefix = "polycythemia"

    class Meta:
        model = Polycythemia
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(PolycythemiaForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy hemoglobin_polycythemia_form %}
                    """
                ),
                id="polycythemia_for_profile",
            ),
        )


class PVDForm(forms.ModelForm):
    prefix = "PVD"

    class Meta:
        model = PVD
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(PVDForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset("", "value", id="PVD_for_profile"),
        )


class ShellfishForm(forms.ModelForm):
    prefix = "shellfish"

    class Meta:
        model = Shellfish
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ShellfishForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Shellfish", "value", id="shellfish_for_profile"),
        )


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
            "date": DateWidget(attrs={"id": "stroke_date.pk"}, usel10n=True, bootstrap_version=3),
        }

    def __init__(self, *args, **kwargs):
        super(StrokeForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Stroke", "value", "number", "date", id="stroke_for_contraindications"),
        )


class StrokeSimpleForm(StrokeForm):
    class Meta:
        model = Stroke
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(StrokeSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="stroke_for_contraindications"),
        )


class TophiForm(forms.ModelForm):
    prefix = "tophi"

    class Meta:
        model = Tophi
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(TophiForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="tophi_for_profile"),
        )


class ThrombocytopeniaForm(forms.ModelForm):
    prefix = "thrombocytopenia"

    class Meta:
        model = Thrombocytopenia
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ThrombocytopeniaForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy platelet_thrombocytopenia_form %}
                    """
                ),
                id="thrombocytopenia_for_profile",
            ),
        )


class ThrombocytosisForm(forms.ModelForm):
    prefix = "thrombocytosis"

    class Meta:
        model = Thrombocytosis
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ThrombocytosisForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                HTML(
                    """
                    {% load crispy_forms_tags %}
                    {% crispy platelet_thrombocytosis_form %}
                    """
                ),
                id="thrombocytosis_for_profile",
            ),
        )


class TransaminitisForm(forms.ModelForm):
    prefix = "transaminitis"

    class Meta:
        model = Transaminitis
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(TransaminitisForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                id="transaminitis_for_profile",
            ),
        )


class UrateKidneyStonesForm(forms.ModelForm):
    prefix = "urate_kidney_stones"

    class Meta:
        model = UrateKidneyStones
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(UrateKidneyStonesForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="urate_kidney_stones_for_profile"),
        )


class XOIInteractionsSimpleForm(forms.ModelForm):
    class Meta:
        model = XOIInteractions
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(XOIInteractionsSimpleForm, self).__init__(*args, **kwargs)
        self.fields["value"].widget = forms.CheckboxInput()
        self.fields["value"].label = "XOI Interactions"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", "value", id="XOIInteractions_for_profile"),
        )


### Family History Forms ###
