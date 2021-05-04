from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit


from .models import Flare
from django import forms

class FlareForm(forms.ModelForm):
    class Meta:
        model = Flare
        fields = ('location', 'treatment', 'colchicine', 'ibuprofen', 'naproxen', 'celecoxib', 'meloxicam', 'prednisone', 'methylprednisolone', 'duration', 'urate_draw', 'urate_log', 'urate')
    
    def __init__(self, *args, **kwargs):
        super(FlareForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Fieldset(
                'Log your flare',
                'location', 
                'treatment', 
                Field('colchicine',),
                Field('ibuprofen'),
                Field('naproxen'), 
                Field('celecoxib'),
                Field('meloxicam'),
                Field('prednisone'),
                Field('methylprednisolone'),
                'duration',
                'urate_draw',
                'urate_log',
                'urate',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )