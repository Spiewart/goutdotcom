from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from datetimewidget.widgets import DateWidget
from django import forms

from .models import (
    Allopurinol,
    Celecoxib,
    Colchicine,
    Ibuprofen,
    Indomethacin,
    Meloxicam,
    Methylprednisolone,
    Naproxen,
    Othertreat,
    Prednisone,
    Tinctureoftime,
)


class AllopurinolForm(forms.ModelForm):
    class Meta:
        model = Allopurinol
        fields = (
            "dose",
            "freq",
            "date_started",
            "side_effects",
        )
        widgets = {
            # Use localization and bootstrap 3
            "date_started": DateWidget(attrs={"id": "allopurinol-date_started"}, usel10n=True, bootstrap_version=3),
        }

    def __init__(self, *args, **kwargs):
        super(AllopurinolForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log an Allopurinol",
                "dose",
                "freq",
                "date_started",
                "side_effects",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class ColchicineForm(forms.ModelForm):
    class Meta:
        model = Colchicine
        fields = (
            "dose",
            "freq",
            "side_effects",
        )

    def __init__(self, *args, **kwargs):
        super(ColchicineForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a Colcrys",
                "dose",
                "freq",
                "side_effects",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class IbuprofenForm(forms.ModelForm):
    class Meta:
        model = Ibuprofen
        fields = (
            "dose",
            "freq",
            "side_effects",
        )

    def __init__(self, *args, **kwargs):
        super(IbuprofenForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log an Advil",
                "dose",
                "freq",
                "side_effects",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class NaproxenForm(forms.ModelForm):
    class Meta:
        model = Naproxen
        fields = (
            "dose",
            "freq",
            "side_effects",
        )

    def __init__(self, *args, **kwargs):
        super(NaproxenForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log an Aleve",
                "dose",
                "freq",
                "side_effects",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class MeloxicamForm(forms.ModelForm):
    class Meta:
        model = Meloxicam
        fields = (
            "dose",
            "freq",
            "side_effects",
        )

    def __init__(self, *args, **kwargs):
        super(MeloxicamForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a Mobic",
                "dose",
                "freq",
                "side_effects",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class CelecoxibForm(forms.ModelForm):
    class Meta:
        model = Celecoxib
        fields = (
            "dose",
            "freq",
            "side_effects",
        )

    def __init__(self, *args, **kwargs):
        super(CelecoxibForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a Celebrex",
                "dose",
                "freq",
                "side_effects",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class PrednisoneForm(forms.ModelForm):
    class Meta:
        model = Prednisone
        fields = (
            "dose",
            "freq",
            "side_effects",
        )

    def __init__(self, *args, **kwargs):
        super(PrednisoneForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Log a prednisone",
                "dose",
                "freq",
                "side_effects",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class MethylprednisoloneForm(forms.ModelForm):
    class Meta:
        model = Methylprednisolone
        fields = (
            "dose",
            "as_injection",
            "freq",
            "side_effects",
        )

    def __init__(self, *args, **kwargs):
        super(MethylprednisoloneForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a methylprednisolone",
                "dose",
                "as_injection",
                "freq",
                "side_effects",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class TinctureoftimeForm(forms.ModelForm):
    class Meta:
        model = Tinctureoftime
        fields = ("duration",)

    def __init__(self, *args, **kwargs):
        super(TinctureoftimeForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a tincture of time",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class OthertreatForm(forms.ModelForm):
    class Meta:
        model = Othertreat
        fields = (
            "name",
            "description",
        )

    def __init__(self, *args, **kwargs):
        super(OthertreatForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a different treatment",
                "name",
                "description",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )


class ColchicineFlareForm(ColchicineForm):
    prefix = "colchicine"

    def __init__(self, *args, **kwargs):
        super(ColchicineFlareForm, self).__init__(*args, **kwargs)
        self.fields["dose"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Colcrys",
                "dose",
                "freq",
                "side_effects",
                id="colchicine_for_flare",
            ),
        )


class IbuprofenFlareForm(IbuprofenForm):
    prefix = "ibuprofen"

    def __init__(self, *args, **kwargs):
        super(IbuprofenFlareForm, self).__init__(*args, **kwargs)
        self.fields["dose"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log an Advil",
                "dose",
                "freq",
                "side_effects",
                id="ibuprofen_for_flare",
            ),
        )


class NaproxenFlareForm(NaproxenForm):
    prefix = "naproxen"

    def __init__(self, *args, **kwargs):
        super(NaproxenFlareForm, self).__init__(*args, **kwargs)
        self.fields["dose"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log an Aleve",
                "dose",
                "freq",
                "side_effects",
                id="naproxen_for_flare",
            ),
        )


class MeloxicamFlareForm(MeloxicamForm):
    prefix = "meloxicam"

    def __init__(self, *args, **kwargs):
        super(MeloxicamFlareForm, self).__init__(*args, **kwargs)
        self.fields["dose"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a Mobic",
                "dose",
                "freq",
                "side_effects",
                id="meloxicam_for_flare",
            ),
        )


class CelecoxibFlareForm(CelecoxibForm):
    prefix = "celecoxib"

    def __init__(self, *args, **kwargs):
        super(CelecoxibFlareForm, self).__init__(*args, **kwargs)
        self.fields["dose"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a Celebrex",
                "dose",
                "freq",
                "side_effects",
                id="celecoxib_for_flare",
            ),
        )


class PrednisoneFlareForm(PrednisoneForm):
    prefix = "prednisone"

    def __init__(self, *args, **kwargs):
        super(PrednisoneFlareForm, self).__init__(*args, **kwargs)
        self.fields["dose"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a prednisone",
                "dose",
                "freq",
                "side_effects",
                id="prednisone_for_flare",
            ),
        )


class MethylprednisoloneFlareForm(MethylprednisoloneForm):
    prefix = "methylprednisolone"

    def __init__(self, *args, **kwargs):
        super(MethylprednisoloneFlareForm, self).__init__(*args, **kwargs)
        self.fields["dose"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a methylprednisolone",
                "dose",
                "as_injection",
                "freq",
                "side_effects",
                id="methylprednisolone_for_flare",
            ),
        )


class TinctureoftimeFlareForm(TinctureoftimeForm):
    prefix = "tinctureoftime"

    def __init__(self, *args, **kwargs):
        super(TinctureoftimeFlareForm, self).__init__(*args, **kwargs)
        self.fields["duration"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a tinctureoftime",
                "duration",
                id="tinctureoftime_for_flare",
            ),
        )


class OthertreatFlareForm(OthertreatForm):
    prefix = "othertreat"

    def __init__(self, *args, **kwargs):
        super(OthertreatFlareForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                "Log a different treatment",
                "name",
                "description",
                id="othertreat_for_flare",
            ),
        )
