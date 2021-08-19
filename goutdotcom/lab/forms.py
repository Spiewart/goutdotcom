from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit

from datetimewidget.widgets import DateTimeWidget

from .models import Urate
from django import forms

class UrateForm(forms.ModelForm):
    class Meta:
        model = Urate
        fields = ('value', 'date_drawn',)
        widgets = {
            #Use localization and bootstrap 3
            'date_drawn': DateTimeWidget(attrs={'id':"date_drawn.pk"}, usel10n = True, bootstrap_version=3)
        }

    def __init__(self, *args, **kwargs):
        super(UrateForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a uric acid',
                'value',
                'date_drawn',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )


class UrateFlareForm(forms.ModelForm):
    class Meta:
        model = Urate
        fields = ('value', 'date_drawn',)
        widgets = {
            #Use localization and bootstrap 3
            'date_drawn': DateTimeWidget(attrs={'id': "date_drawn.pk"}, usel10n=True, bootstrap_version=3)
        }

    def __init__(self, *args, **kwargs):
        super(UrateFlareForm, self).__init__(*args, **kwargs)
        self.fields['value'].required = False
        self.fields['date_drawn'].required = False
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log a uric acid',
                'value',
                'date_drawn',
                id='urate_fields',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
