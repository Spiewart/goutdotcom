from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit


from .models import Colchicine, Ibuprofen, Naproxen, Celecoxib, Meloxicam, Prednisone, Methylprednisolone
from django import forms

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


class ColchicineFlareForm(forms.ModelForm):
    class Meta:
        model = Colchicine
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(ColchicineFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        self.fields['freq'].required = False
        self.fields['date_started'].required = False
        self.fields['date_ended'].required = False
        self.fields['side_effects'].required = False

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


class IbuprofenFlareForm(forms.ModelForm):
    class Meta:
        model = Ibuprofen
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(IbuprofenFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        self.fields['freq'].required = False
        self.fields['date_started'].required = False
        self.fields['date_ended'].required = False
        self.fields['side_effects'].required = False

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


class NaproxenFlareForm(forms.ModelForm):
    class Meta:
        model = Naproxen
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(NaproxenFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        self.fields['freq'].required = False
        self.fields['date_started'].required = False
        self.fields['date_ended'].required = False
        self.fields['side_effects'].required = False

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


class MeloxicamFlareForm(forms.ModelForm):
    class Meta:
        model = Meloxicam
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(MeloxicamFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        self.fields['freq'].required = False
        self.fields['date_started'].required = False
        self.fields['date_ended'].required = False
        self.fields['side_effects'].required = False

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


class CelecoxibFlareForm(forms.ModelForm):
    class Meta:
        model = Celecoxib
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(CelecoxibFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        self.fields['freq'].required = False
        self.fields['date_started'].required = False
        self.fields['date_ended'].required = False
        self.fields['side_effects'].required = False

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


class PrednisoneFlareForm(forms.ModelForm):
    class Meta:
        model = Prednisone
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(PrednisoneFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        self.fields['freq'].required = False
        self.fields['date_started'].required = False
        self.fields['date_ended'].required = False
        self.fields['side_effects'].required = False

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


class MethylprednisoloneFlareForm(forms.ModelForm):
    class Meta:
        model = Methylprednisolone
        fields = ('dose', 'freq', 'date_started', 'date_ended', 'side_effects',)

    def __init__(self, *args, **kwargs):
        super(MethylprednisoloneFlareForm, self).__init__(*args, **kwargs)
        self.fields['dose'].required = False
        self.fields['freq'].required = False
        self.fields['date_started'].required = False
        self.fields['date_ended'].required = False
        self.fields['side_effects'].required = False

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
