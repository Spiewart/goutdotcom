from goutdotcom.profiles.forms import PatientProfileForm
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse

from .models import PatientProfile
from goutdotcom.vitals.forms import HeightForm, WeightForm
from goutdotcom.vitals.models import Height, Weight

# Create your views here.
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
        context.update({
            'user': self.request.user
        })
        if 'height_form' not in context:
            context['height_form'] = self.height_form_class(self.request.GET)
        if 'weight_form' not in context:
            context['weight_form'] = self.weight_form_class(self.request.GET)
        return context

    def get_object(self, queryset=None):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=PatientProfile())
        height_form = self.height_form_class(request.POST, instance=Height())
        weight_form = self.weight_form_class(request.POST, instance=Weight())

        if form.is_valid():
            profile_data = form.save(commit=False)
            profile_data.user = request.user
            if height_form.is_valid():
                height_data = height_form.save(commit=False)
                height_data.user = request.user
                height_data.save()
                profile_data.height = height_data
            if weight_form.is_valid():
                weight_data = weight_form.save(commit=False)
                weight_data.user = request.user
                weight_data.save()
                profile_data.weight = weight_data
            profile_data.save()
            return HttpResponseRedirect(reverse('users:detail', kwargs={'user': auth.get_user(request)}))
        else:
            return self.render_to_response(
                self.get_context_data(form=form, height_form=height_form, weight_form=weight_form))

class PatientProfileUpdate(LoginRequiredMixin, UpdateView):
    model = PatientProfile
    form_class = PatientProfileForm
    height_form_class = HeightForm
    weight_form_class = WeightForm

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PatientProfileUpdate, self).get_context_data(**kwargs)
        context.update({
            'user': self.request.user
        })
        if 'height_form' not in context:
            context['height_form'] = self.height_form_class(self.request.GET)
        if 'weight_form' not in context:
            context['weight_form'] = self.weight_form_class(self.request.GET)
        return context

    def get_object(self, queryset=None):
        model = self.model
        try:
            queryset = model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")

        obj = super(PatientProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def get(self, request, *args, **kwargs):
        super(PatientProfileUpdate, self).get(request, *args, **kwargs)
        form = self.form_class
        height_form = self.height_form_class
        weight_form = self.weight_form_class
        return self.render_to_response(self.get_context_data(
            form=form, height_form=height_form, weight_form=weight_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, self.object)
        height_form = self.height_form_class(request.POST)
        weight_form = self.weight_form_class(request.POST)

        if form.is_valid() and height_form.is_valid() and weight_form.is_valid():
            profile_data = form.save(commit=False)
            profile_data.user = request.user
            height_data = height_form.save(commit=False)
            height_data.user = request.user
            weight_data = weight_form.save(commit=False)
            weight_data.user = request.user
            height_data.save()
            weight_data.save()
            profile_data.height = height_data
            profile_data.weight = weight_data
            profile_data.save()
            return HttpResponseRedirect(reverse('users:detail', kwargs={'user':request.user}))
        else:
            return self.render_to_response(
                self.get_context_data(profile_form=form, height_form=height_form, weight_form=weight_form))

"""class PatientProfileUpdate(LoginRequiredMixin, UpdateView):
    model = PatientProfile
    height_model = Height
    weight_model = Weight
    form_class_profile = PatientProfileForm
    form_class_height = HeightForm
    form_class_weight = WeightForm
    fields = ['picture',
              'date_of_birth',
              'gender',
              'race',
              'weight',
              'height',
              ]

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PatientProfileUpdate, self).get_context_data(**kwargs)
        context.update({
            'user': self.request.user
        })
        if 'profile_form' not in context:
            context['profile_form'] = self.form_class_profile(self.request.GET, instance=self.object)
        if 'height_form' not in context:
            context['height_form'] = self.form_class_height(self.request.GET)
        if 'weight_form' not in context:
            context['weight_form'] = self.form_class_weight(self.request.GET)
        return context

    def get(self, request, *args, **kwargs):
        super(PatientProfileUpdate, self).get(request, *args, **kwargs)
        profile_form = self.form_class_profile
        height_form = self.form_class_height
        weight_form = self.form_class_weight
        return self.render_to_response(self.get_context_data(
           'profile_form'=profile_form, 'height_form'=height_form, 'weight_form'=weight_form))

    def get_object(self, queryset=None):
        model = self.model
        try:
            queryset = model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")

        obj = super(PatientProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.height_model.objects.get(user=request.user, pk=self.object.height.pk)
        self.weight_model.objects.get(user=request.user, pk=self.object.weight.pk)
        profile_form = self.form_class_profile(request.POST, self.object)
        height_form = self.form_class_height(request.POST, self.height_model)
        weight_form = self.form_class_weight(request.POST, self.weight_model)

        if profile_form.is_valid() and height_form.is_valid() and weight_form.is_valid():
            profile_data = profile_form.save(commit=False)
            profile_data.user = request.user
            height_data = height_form.save(commit=False)
            height_data.user = request.user
            weight_data = weight_form.save(commit=False)
            weight_data.user = request.user
            height_data.save()
            weight_data.save()
            profile_data.height = height_data
            profile_data.weight = weight_data
            profile_data.save()
            return HttpResponseRedirect(reverse('users:detail', kwargs={'user':request.user}))
        else:
            return self.render_to_response(
                self.get_context_data(profile_form=profile_form, height_form=height_form, weight_form=weight_form))"""
