from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import modelform_factory
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import ULTForm
from .models import ULT

# Create your views here.


class ULTCreate(CreateView):
    model = ULT
    form_class = ULTForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                user_ULT = self.model.objects.get(user=self.request.user)
            except self.model.DoesNotExist:
                user_ULT = None
            if user_ULT:
                return redirect("ult:update", pk=self.model.objects.get(user=self.request.user).pk)
            else:
                return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    def get_form_class(self):
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured("Specifying both 'fields' and 'form_class' is not permitted.")
        if self.form_class:
            return self.form_class
        else:
            if self.request.user.medicalprofile.ckd is not None:
                # Check if User has endorsed whether or not they have CKD in MedicalProfile
                self.fields.pop("ckd")
            else:
                model = self.get_queryset().model
            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )
            return modelform_factory(model, fields=self.fields)


class ULTDetail(DetailView):
    model = ULT


class ULTUpdate(LoginRequiredMixin, UpdateView):
    model = ULT
    form_class = ULTForm
