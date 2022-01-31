from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Fieldset, Layout, Submit
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {"username": {"unique": _("This username has already been taken.")}}


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["role"]

    def signup(self, request, user):
        user.role = self.cleaned_data["role"]
        user.save()


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email",]

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                "username",
                "email",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )
