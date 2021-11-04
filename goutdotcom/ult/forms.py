from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Fieldset, Layout, Submit
from django import forms

from .models import ULT


class ULTForm(forms.ModelForm):
    erosions = forms.BooleanField(required=False, help_text="Do you have erosions on x-rays or other imaging?")
    tophi = forms.BooleanField(required=False, help_text="Do you have gouty tophi?")
    stones = forms.BooleanField(required=False, help_text="Do you get uric acid kidney stones?")
    ckd = forms.BooleanField(required=False, help_text="Do you have chronic kidney disease (CKD)?")
    uric_acid = forms.BooleanField(required=False, help_text="Is your uric acid over 9.0?")

    class Meta:
        model = ULT
        fields = ("num_flares", "freq_flares", "erosions", "tophi", "stones", "ckd", "uric_acid")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # pop the 'user' from kwargs dictionary
        super(ULTForm, self).__init__(*args, **kwargs)
        self.fields["ckd"].label = "CKD"
        # check if user isn't logged in (anonymous if not)
        if user.is_anonymous != True:
            # removes ckd from fields if pulling value from MedicalProfile
            if user.medicalprofile.CKD.value == True:
                self.fields.pop("ckd")
            if user.medicalprofile.CKD.value == False:
                self.fields.pop("ckd")
            # removes stones from fields if pulling value from MedicalProfile
            if user.medicalprofile.urate_kidney_stones.value == True:
                self.fields.pop("stones")
            if user.medicalprofile.urate_kidney_stones.value == False:
                self.fields.pop("stones")
            # removes erosions from fields if pulling value from MedicalProfile
            if user.medicalprofile.erosions.value == True:
                self.fields.pop("erosions")
            if user.medicalprofile.erosions.value == False:
                self.fields.pop("erosions")
            # removes tophi from fields if pulling value from MedicalProfile
            if user.medicalprofile.tophi.value == True:
                self.fields.pop("tophi")
            if user.medicalprofile.tophi.value == False:
                self.fields.pop("tophi")
            # removes uric_acid from fields if pulling value from MedicalProfile
            if user.medicalprofile.hyperuricemia.value == True:
                self.fields.pop("uric_acid")
            if user.medicalprofile.hyperuricemia.value == False:
                self.fields.pop("uric_acid")
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                "",
                "num_flares",
                "freq_flares",
                HTML(
                    """
                    <div id="follow-up-questions">
                    <hr size="6" color="white">
                    <h3>Do you have any of the following?:</h3>
                    </div>
                    """
                ),
                "erosions",
                "tophi",
                "stones",
                "ckd",
                "uric_acid",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
        if user.is_anonymous != True:
            # removes ckd from Fieldset if pulling value from MedicalProfile
            if user.medicalprofile.CKD.value == True:
                self.helper.layout[0].remove("ckd")
            if user.medicalprofile.CKD.value == False:
                self.helper.layout[0].remove("ckd")
            # removes stones from Fieldset if pulling value from MedicalProfile
            if user.medicalprofile.urate_kidney_stones.value == True:
                self.helper.layout[0].remove("stones")
            if user.medicalprofile.urate_kidney_stones.value == False:
                self.helper.layout[0].remove("stones")
            # removes erosions from Fieldset if pulling value from MedicalProfile
            if user.medicalprofile.erosions.value == True:
                self.helper.layout[0].remove("erosions")
            if user.medicalprofile.erosions.value == False:
                self.helper.layout[0].remove("erosions")
            # removes tophi from Fieldset if pulling value from MedicalProfile
            if user.medicalprofile.tophi.value == True:
                self.helper.layout[0].remove("tophi")
            if user.medicalprofile.tophi.value == False:
                self.helper.layout[0].remove("tophi")
            # removes uric_acid from Fieldset if pulling value from MedicalProfile
            if user.medicalprofile.hyperuricemia.value == True:
                self.helper.layout[0].remove("uric_acid")
            if user.medicalprofile.hyperuricemia.value == False:
                self.helper.layout[0].remove("uric_acid")
            if user.medicalprofile.CKD.value == True:
                # and user.medicalprofile.urate_kidney_stones.value
                # and user.medicalprofile.erosions.value
                # and user.medicalprofile.tophi.value
                # and user.medicalprofile.hyperuricemia.value
                # ):
                for item in self.helper.layout[0]:
                    print(item)
                del self.helper.layout[0][2]
