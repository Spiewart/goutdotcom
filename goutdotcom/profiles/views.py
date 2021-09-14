from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from goutdotcom.profiles.forms import PatientProfileForm
from goutdotcom.vitals.forms import HeightForm, WeightForm
from goutdotcom.vitals.models import Height, Weight

from .models import MedicalProfile, PatientProfile


# Create your views here.
class MedicalProfileCreate(LoginRequiredMixin, CreateView):
    model = MedicalProfile
    form_class = MedicalProfileForm
    CKD_form_class = CKDForm
    hypertension_form_class = HypertensionForm
    CHF_form_class = CHFForm
    diabetes_form_class = DiabetesForm
    urate_kidney_stone_form_class = UrateKidneyStoneForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PatientProfileCreate(LoginRequiredMixin, CreateView):
    model = PatientProfile
    form_class = PatientProfileForm
    height_form_class = HeightForm
    weight_form_class = WeightForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PatientProfileCreate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if "height_form" not in context:
            context["height_form"] = self.height_form_class(self.request.GET)
        if "weight_form" not in context:
            context["weight_form"] = self.weight_form_class(self.request.GET)
        return context

    def get_object(self, queryset=None):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=PatientProfile())
        height_form = self.height_form_class(request.POST, instance=Height())
        weight_form = self.weight_form_class(request.POST, instance=Weight())

        if form.is_valid() and height_form.is_valid() and weight_form.is_valid():
            profile_data = form.save(commit=False)
            profile_data.user = request.user
            height_data = height_form.save(commit=False)
            height_data.user = request.user
            height_data.save()
            weight_data = weight_form.save(commit=False)
            weight_data.user = request.user
            weight_data.save()
            profile_data.height = height_data
            profile_data.weight = weight_data
            profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, height_form=height_form, weight_form=weight_form)
            )


class PatientProfileUpdate(LoginRequiredMixin, UpdateView):
    model = PatientProfile
    form_class = PatientProfileForm
    height_form_class = HeightForm
    weight_form_class = WeightForm

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PatientProfileUpdate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if self.request.POST:
            context["height_form"] = HeightForm(self.request.POST, instance=self.object.height)
            context["weight_form"] = WeightForm(self.request.POST, instance=self.object.weight)
        else:
            context["height_form"] = self.height_form_class(instance=self.object.height)
            context["weight_form"] = self.weight_form_class(instance=self.object.weight)
        return context

    def get_object(self, queryset=None):
        try:
            queryset = self.model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(PatientProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        # NEED **kwargs even though VSCode IDE says it's not used. Can't accept <user> and <pk> from url parameter otherwise.
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        height_form = self.height_form_class(request.POST, instance=self.object.height)
        weight_form = self.weight_form_class(request.POST, instance=self.object.weight)

        if form.is_valid() and height_form.is_valid() and weight_form.is_valid():
            profile_data = form.save(commit=False)
            if "value" in height_form.changed_data:
                height_data = height_form.save(commit=False)
                height_data.pk = None
                height_data.save()
                weight_data = weight_form.save()
            elif "value" in weight_form.changed_data:
                height_data = height_form.save()
                weight_data = weight_form.save(commit=False)
                weight_data.pk = None
                weight_data.save()
            elif "value" in height_form.changed_data and "value" in weight_form.changed_data:
                height_data = height_form.save(commit=False)
                height_data.pk = None
                height_data.save()
                weight_data = weight_form.save(commit=False)
                weight_data.pk = None
                weight_data.save()
            else:
                height_data = height_form.save(commit=False)
                height_data.save()
                weight_data = weight_form.save(commit=False)
                weight_data.save()
            profile_data.height = height_data
            profile_data.weight = weight_data
            profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, height_form=height_form, weight_form=weight_form)
            )
