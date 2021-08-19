from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from django import forms

from .models import Allopurinol, Colchicine, Ibuprofen, Naproxen, Celecoxib, Meloxicam, Prednisone, Methylprednisolone, Tinctureoftime, Othertreat
from .choices import COLCHICINE_DOSE_CHOICES, IBUPROFEN_DOSE_CHOICES, MELOXICAM_DOSE_CHOICES, NAPROXEN_DOSE_CHOICES, METHYLPREDNISOLONE_DOSE_CHOICES, CELECOXIB_DOSE_CHOICES

class AllopurinolForm(forms.ModelForm):
    class Meta:
        model = Allopurinol
        fields = ('dose', 'freq', 'date_started', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(AllopurinolForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a Colcrys',
                'dose',
                'freq',
                'date_started',
                'side_effects',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class ColchicineForm(forms.ModelForm):
    class Meta:
        model = Colchicine
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(ColchicineForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a Colcrys',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class IbuprofenForm(forms.ModelForm):
    class Meta:
        model = Ibuprofen
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(IbuprofenForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log an Advil',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class NaproxenForm(forms.ModelForm):
    class Meta:
        model = Naproxen
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(NaproxenForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log an Aleve',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class MeloxicamForm(forms.ModelForm):
    class Meta:
        model = Meloxicam
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(MeloxicamForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a Mobic',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class CelecoxibForm(forms.ModelForm):
    class Meta:
        model = Celecoxib
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(CelecoxibForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a Celebrex',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class PrednisoneForm(forms.ModelForm):
    class Meta:
        model = Prednisone
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(PrednisoneForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a prednisone',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class MethylprednisoloneForm(forms.ModelForm):
    class Meta:
        model = Methylprednisolone
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(MethylprednisoloneForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a methylprednisolone',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class TinctureoftimeForm(forms.ModelForm):
    class Meta:
        model = Tinctureoftime
        fields = ('date_started', 'date_ended',)

    def __init__(self, *args, **kwargs):
        super(TinctureoftimeForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a tincture of time',
                'date_started',
                'date_ended',

                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class OthertreatForm(forms.ModelForm):
    class Meta:
        model = Othertreat
        fields = ('name', 'description',)

    def __init__(self, *args, **kwargs):
        super(OthertreatForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a different treatment',
                'name',
                'description',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )

class ColchicineFlareForm(forms.ModelForm):
    prefix = 'colchicine'

    class Meta:
        model = Colchicine
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(ColchicineFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a Colcrys',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                id='colchicine_for_flare',
            ),
        )


class IbuprofenFlareForm(forms.ModelForm):
    prefix = 'ibuprofen'

    class Meta:
        model = Ibuprofen
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(IbuprofenFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log an Advil',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                id='ibuprofen_for_flare',
            ),
        )


class NaproxenFlareForm(forms.ModelForm):
    prefix = 'naproxen'

    class Meta:
        model = Naproxen
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(NaproxenFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log an Aleve',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                id='naproxen_for_flare',
            ),
        )


class MeloxicamFlareForm(forms.ModelForm):
    prefix = 'meloxicam'

    class Meta:
        model = Meloxicam
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(MeloxicamFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a Mobic',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                id='meloxicam_for_flare',
            ),
        )


class CelecoxibFlareForm(forms.ModelForm):
    prefix = 'celecoxib'

    class Meta:
        model = Celecoxib
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(CelecoxibFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a Celebrex',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                id='celecoxib_for_flare',
            ),
        )


class PrednisoneFlareForm(forms.ModelForm):
    prefix = 'prednisone'

    class Meta:
        model = Prednisone
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(PrednisoneFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a prednisone',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                id='prednisone_for_flare',
            ),
        )


class MethylprednisoloneFlareForm(forms.ModelForm):
    prefix = 'methylprednisolone'

    class Meta:
        model = Methylprednisolone
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(MethylprednisoloneFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a methylprednisolone',
                'dose',
                'freq',
                'date_started',
                'date_ended',
                'side_effects',
                id='methylprednisolone_for_flare',
            ),
        )

class TinctureoftimeFlareForm(forms.ModelForm):
    prefix = 'tinctureoftime'

    class Meta:
        model = Tinctureoftime
        fields = ('duration', 'date_started', 'date_ended',)

    def __init__(self, *args, **kwargs):
        super(TinctureoftimeFlareForm, self).__init__(*args, **kwargs)
        self.fields['duration'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a tinctureoftime',
                'date_started',
                'date_ended',
                id='tinctureoftime_for_flare',
            ),
        )

class OthertreatFlareForm(forms.ModelForm):
    prefix='othertreat'

    class Meta:
        model = Othertreat
        fields = ('name', 'description', )

    def __init__(self, *args, **kwargs):
        super(OthertreatFlareForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a different treatment',
                'name',
                'description',
                id='othertreat_for_flare',
            ),
        )
