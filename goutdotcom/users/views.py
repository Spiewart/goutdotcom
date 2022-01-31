from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, RedirectView, UpdateView

from .forms import UserCreateForm

User = get_user_model()

class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'users.can_add_patient'
    model = User
    form_class = UserCreateForm
    template_name = "users/provideruser_form.html"

    def form_valid(self, form):
        form.instance.role = "PATIENT"
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.user.get_absolute_url()


user_create_view = UserCreateView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):

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
