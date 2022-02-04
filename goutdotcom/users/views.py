from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)

from ..utils.mixins import PatientProviderUserMixin
from .forms import UserCreateForm
from .models import Patient

User = get_user_model()


class ProviderPatientListView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, ListView):
    """ListView for displaying all of a Provider's Patients."""

    permission_required = "users.can_view_patient"
    model = User
    template_name = "users/providerpatient_list.html"
    paginate_by = 5

    # Test whether User is Provider, if not raise 404
    def test_func(self):
        return self.request.user.role == "PROVIDER"

    # Overwrite get_queryset() to return Patient objects filtered by their PatientProfile provider field
    # Fetch only Patients where the provider is equal to the requesting User (Provider)
    def get_queryset(self):
        return Patient.objects.filter(patientprofile__provider=self.request.user)


provider_patient_list_view = ProviderPatientListView.as_view()


class UserCreateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    """View only for Providers to create Patients.
    Assigns Patient provider field to the creating Provider.

    Returns:
        [redirect]: [Redirects to the newly created Patient's Detail page.]
    """

    model = User
    form_class = UserCreateForm
    template_name = "users/provideruser_form.html"

    def test_func(self):
        return self.request.user.role == "PROVIDER"

    def form_valid(self, form):
        # Assign finished form to variable user
        user = form.save(commit=False)
        # If logged in User is a Provider
        if self.request.user.role == "PROVIDER":
            # Assign user from form a role of Patient
            user.role = "PATIENT"
            # Save user, which will trigger post_save() creating Profiles, including PatientProfile
            user.save()
            # Assign logged in Provider User to user.patientprofile.provider field
            user.patientprofile.provider = self.request.user
            # Save user.patientprofile
            user.patientprofile.save()
            # Redirect to newly created Patient's detail page
        return HttpResponseRedirect(reverse("users:detail", kwargs={"username": user.username}))


user_create_view = UserCreateView.as_view()


class UserDetailView(LoginRequiredMixin, PatientProviderUserMixin, DetailView):
    """Detail View for Users.
    PatientProviderUserMixin checks role of user, determines access accordingly.
    """

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["patients"] = User.objects.filter(patientprofile__provider=self.request.user)
        return context


user_detail_view = UserDetailView.as_view()


class UserProviderDetailView(LoginRequiredMixin, DetailView):

    model = User


user_provider_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserProviderUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("User successfully updated")


user_provider_update_view = UserProviderUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
