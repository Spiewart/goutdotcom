from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Field, Fieldset, Layout, Submit
from django import forms

from .models import ALT, AST, WBC, Creatinine, Hemoglobin, LabCheck, Platelet, Urate


class ALTForm(forms.ModelForm):
    class Meta:
        model = ALT
        fields = (
            "value",
            "date_drawn",
        )

    def __init__(self, *args, **kwargs):
        super(ALTForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "ALT",
                "value",
                "date_drawn",
            ),
        )


class ASTForm(forms.ModelForm):
    class Meta:
        model = AST
        fields = (
            "value",
            "date_drawn",
        )

    def __init__(self, *args, **kwargs):
        super(ASTForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "AST",
                "value",
                "date_drawn",
            ),
        )


class CreatinineForm(forms.ModelForm):
    class Meta:
        model = Creatinine
        fields = (
            "value",
            "date_drawn",
        )

    def __init__(self, *args, **kwargs):
        super(CreatinineForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Creatinine",
                "value",
                "date_drawn",
            ),
        )


class HemoglobinForm(forms.ModelForm):
    class Meta:
        model = Hemoglobin
        fields = (
            "value",
            "date_drawn",
        )

    def __init__(self, *args, **kwargs):
        super(HemoglobinForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Hemoglobin",
                "value",
                "date_drawn",
            ),
        )


class LabCheckForm(forms.ModelForm):
    """Form for creating new lab check and related lab models."""

    class Meta:
        model = LabCheck
        fields = ()

    def __init__(self, *args, **kwargs):
        super(LabCheckForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "",
            ),
        )


class PlateletForm(forms.ModelForm):
    class Meta:
        model = Platelet
        fields = (
            "value",
            "date_drawn",
        )

    def __init__(self, *args, **kwargs):
        super(PlateletForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Platelet",
                "value",
                "date_drawn",
            ),
        )


class WBCForm(forms.ModelForm):
    class Meta:
        model = WBC
        fields = (
            "value",
            "date_drawn",
        )

    def __init__(self, *args, **kwargs):
        super(WBCForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "WBC",
                "value",
                "date_drawn",
            ),
        )


class UrateForm(forms.ModelForm):
    class Meta:
        model = Urate
        fields = (
            "value",
            "date_drawn",
        )

    def __init__(self, *args, **kwargs):
        super(UrateForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Uric acid",
                "value",
                "date_drawn",
            ),
        )


class UrateFlareForm(UrateForm):
    prefix = "urate"

    class Meta:
        model = Urate
        fields = ("value",)
        widgets = {
            "value": forms.NumberInput(attrs={"step": 0.10}),
        }

    def __init__(self, *args, **kwargs):
        super(UrateFlareForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = "Do you know what your uric acid was during your flare?"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
                id="urate_fields",
            ),
        )
