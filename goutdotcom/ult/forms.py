from goutdotcom.goutdotcom.ult.models import ULT
from django import forms

class ULTForm(forms.ModelForm):
    first_flare = forms.BooleanField(initial=True)

    class Meta:
        model = ULT
        fields = '__all__'
