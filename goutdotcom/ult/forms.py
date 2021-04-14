from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField


from .models import ULT
from django import forms

class ULTForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ULTForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            MultiField(
                'Answer this to sort it out',
                'first_flare', 
                'num_flares', 
                'freq_flares', 
                'erosions', 
                'tophi', 
                'stones', 
                'ckd', 
                'uric_acid',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
        )
        
    class Meta:
        model = ULT
        fields = ('first_flare', 'num_flares', 'freq_flares', 'erosions', 'tophi', 'stones', 'ckd', 'uric_acid')
        
    