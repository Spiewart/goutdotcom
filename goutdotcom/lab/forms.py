from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Field, Fieldset, Layout, Submit
from django import forms

from .models import ALT, AST, WBC, Creatinine, Hemoglobin, LabCheck, Platelet, Urate


class ALTForm(forms.ModelForm):
    prefix = "ALT"

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


class ALTProfileForm(ALTForm):
    class Meta:
        model = ALT
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ALTProfileForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = "ALT"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                "value",
            ),
        )


class ASTForm(forms.ModelForm):
    prefix = "AST"

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


class ASTProfileForm(ASTForm):
    class Meta:
        model = AST
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(ASTProfileForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = "AST"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "AST",
                "value",
            ),
        )


class CreatinineForm(forms.ModelForm):
    prefix = "creatinine"

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


class CreatinineProfileForm(CreatinineForm):
    class Meta:
        model = Creatinine
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(CreatinineProfileForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = "Creatinine"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Creatinine",
                "value",
            ),
        )


class HemoglobinForm(forms.ModelForm):
    prefix = "hemoglobin"

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


class HemoglobinProfileForm(HemoglobinForm):
    class Meta:
        model = Hemoglobin
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(HemoglobinProfileForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = "Hemoglobin"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Hemoglobin",
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
    prefix = "platelet"

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


class PlateletProfileForm(PlateletForm):
    class Meta:
        model = Platelet
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(PlateletProfileForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = "Platelets"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Platelet",
                "value",
            ),
        )


class WBCForm(forms.ModelForm):
    prefix = "wbc"

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


class WBCProfileForm(WBCForm):
    class Meta:
        model = WBC
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super(WBCProfileForm, self).__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].label = "WBC"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "WBC",
                "value",
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
