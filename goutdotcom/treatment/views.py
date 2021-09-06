from .forms import *
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import modelform_factory
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from .models import Allopurinol, Colchicine, Febuxostat, Ibuprofen, Celecoxib, Meloxicam, Naproxen, Prednisone, Probenecid, Methylprednisolone, Tinctureoftime, Othertreat

non_prn_models = [Allopurinol, Febuxostat, Probenecid]
allopurinol_model = [Allopurinol]
prn_models = [Colchicine, Ibuprofen, Naproxen, Meloxicam, Celecoxib, Prednisone, Methylprednisolone, Tinctureoftime, Othertreat]
injection_models = [Methylprednisolone]

class TreatmentAbout(TemplateView):
    def get_template_names(self, **kwargs):
        kwargs = self.kwargs
        treatment = kwargs.get('treatment')
        template = "treatment/" + str(treatment) + "_about.html"
        return template

    def get_context_data(self, **kwargs):
        context = super(TreatmentAbout, self).get_context_data(**kwargs)
        context.update({
            'treatment': self.kwargs['treatment'],
        })
        return context

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'treatment/dashboard.html'
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'allopurinol_list': Allopurinol.objects.filter(user=self.request.user),
            'febuxostat_list': Febuxostat.objects.filter(user=self.request.user),
            'colchicine_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=False).order_by('-created')[:1],
            'ibuprofen_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=False).order_by('-created')[:1],
            'celecoxib_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=False).order_by('-created')[:1],
            'meloxicam_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=False).order_by('-created')[:1],
            'naproxen_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=False).order_by('-created')[:1],
            'prednisone_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=False).order_by('-created')[:1],
            'probenecid_list': Probenecid.objects.filter(user=self.request.user),
            'methylprednisolone_list': Methylprednisolone.objects.filter(user=self.request.user).order_by('-created')[:1],
            'colchicine_ppx_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=True),
            'ibuprofen_ppx_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=True),
            'celecoxib_ppx_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=True),
            'meloxicam_ppx_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=True),
            'naproxen_ppx_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=True),
            'prednisone_ppx_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=True),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'treatment/index.html'
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'allopurinol_list': Allopurinol.objects.filter(user=self.request.user),
            'febuxostat_list': Febuxostat.objects.filter(user=self.request.user),
            'colchicine_list': Colchicine.objects.filter(user=self.request.user),
            'ibuprofen_list': Ibuprofen.objects.filter(user=self.request.user),
            'celecoxib_list': Celecoxib.objects.filter(user=self.request.user),
            'meloxicam_list': Meloxicam.objects.filter(user=self.request.user),
            'naproxen_list': Naproxen.objects.filter(user=self.request.user),
            'prednisone_list': Prednisone.objects.filter(user=self.request.user),
            'probenecid_list': Probenecid.objects.filter(user=self.request.user),
            'methylprednisolone_list': Methylprednisolone.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class FlareView(LoginRequiredMixin, ListView):
    template_name = 'treatment/flare.html'
    model = Colchicine

    def get_context_data(self, **kwargs):
        context = super(FlareView, self).get_context_data(**kwargs)
        context.update({
            'colchicine_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=False),
            'ibuprofen_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=False),
            'celecoxib_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=False),
            'meloxicam_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=False),
            'naproxen_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=False),
            'prednisone_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=False),
            'methylprednisolone_list': Methylprednisolone.objects.filter(user=self.request.user, as_injection=True),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ULTView(LoginRequiredMixin, ListView):
    template_name = 'treatment/ult.html'
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(ULTView, self).get_context_data(**kwargs)
        context.update({
            'allopurinol_list': Allopurinol.objects.filter(user=self.request.user),
            'febuxostat_list': Febuxostat.objects.filter(user=self.request.user),
            'probenecid_list': Probenecid.objects.filter(user=self.request.user),
            'colchicine_ppx_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=True),
            'ibuprofen_ppx_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=True),
            'celecoxib_ppx_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=True),
            'meloxicam_ppx_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=True),
            'naproxen_ppx_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=True),
            'prednisone_ppx_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=True),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class TreatmentCreate(LoginRequiredMixin, CreateView):
    fields = ['dose', 'freq', 'side_effects']

    def get(self, request, *args, **kwargs):
        self.object = None
        self.treatment = self.kwargs['treatment']
        self.model = apps.get_model('treatment', model_name=self.treatment)
        if self.model in self.non_prn_models:
            try:
                user_treatment = self.model.objects.get(user=self.request.user)
            except self.model.DoesNotExist:
                user_treatment = None
            if user_treatment:
                return redirect("treatment:update", treatment=self.kwargs['treatment'], pk=self.model.objects.get(user=self.request.user).pk)
            else:
                return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    def get_form_class(self):
        self.treatment = self.kwargs['treatment']
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            return self.form_class
        else:
            if self.treatment is not None:
                # Fetch model from URL 'lab' parameter
                model = apps.get_model('treatment', model_name=self.treatment)
                if model in prn_models:
                    self.fields.append('prn')
                    self.fields.append('date_started')
                    self.fields.append('date_ended')
                if model in allopurinol_model:
                    self.fields.append('de_sensitized')
                if model in injection_models:
                    self.fields.append('as_injection')
            elif getattr(self, 'object', None) is not None:
                model = self.object.__class__
            else:
                model = self.get_queryset().model
            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )
            return modelform_factory(model, fields = self.fields)

    def get_template_names(self):
        template = "treatment/treatment_form.html"
        return template

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TreatmentCreate, self).get_context_data(**kwargs)
        context.update({
            'treatment': self.kwargs['treatment'],
        })
        return context

class TreatmentDetail(LoginRequiredMixin, DetailView):
    def get_object(self):
        self.model = apps.get_model('treatment', model_name=self.kwargs['treatment'])
        treatment = get_object_or_404(self.model, pk=self.kwargs['pk'], user=self.request.user)
        return treatment

    def get_template_names(self):
        template = "treatment/treatment_detail.html"
        return template

class TreatmentList(LoginRequiredMixin, ListView):
    paginate_by = 5

    def get_queryset(self):
        self.model = apps.get_model('treatment', model_name=self.kwargs['treatment'])
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.filter(user=self.request.user).order_by('-created')
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset.filter(user=self.request.user).order_by('-created')

    def get_template_names(self):
        template = "treatment/treatment_list.html"
        return template

    def get_context_data(self, **kwargs):
        self.model = apps.get_model('treatment', model_name=self.kwargs['treatment'])
        context = super(TreatmentList, self).get_context_data(**kwargs)
        context.update({
            'treatment': self.kwargs['treatment'],
        })
        return context

class TreatmentUpdate(LoginRequiredMixin, UpdateView):
    fields = ['dose', 'freq', 'side_effects', 'prn', 'date_started', 'date_ended', 'de_sensitized', 'as_injection',]

    def get(self, request, *args, **kwargs):
        self.treatment = self.kwargs['treatment']
        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        self.treatment = self.kwargs['treatment']
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            model = apps.get_model('treatment', model_name=self.treatment)
            if model not in prn_models:
                if 'prn' in self.fields:
                    self.fields.remove('prn')
                if 'date_started' in self.fields:
                    self.fields.remove('date_started')
                if 'date_ended' in self.fields:
                    self.fields.remove('date_ended')
            if model not in allopurinol_model:
                if 'de_sensitized' in self.fields:
                    self.fields.remove('de_sensitized')
            if model not in injection_models:
                if 'as_injection' in self.fields:
                    self.fields.remove('as_injection')
            return self.form_class
        else:
            if self.treatment is not None:
                # Fetch model from URL 'treatment' parameter
                model = apps.get_model('treatment', model_name=self.treatment)
                if model not in prn_models:
                    if 'prn' in self.fields:
                        self.fields.remove('prn')
                    if 'date_started' in self.fields:
                        self.fields.remove('date_started')
                    if 'date_ended' in self.fields:
                        self.fields.remove('date_ended')
                if model not in allopurinol_model:
                    if 'de_sensitized' in self.fields:
                        self.fields.remove('de_sensitized')
                if model not in injection_models:
                    if 'as_injection' in self.fields:
                        self.fields.remove('as_injection')
            elif getattr(self, 'object', None) is not None:
                model = self.object.__class__
                if model not in prn_models:
                    if 'prn' in self.fields:
                        self.fields.remove('prn')
                    if 'date_started' in self.fields:
                        self.fields.remove('date_started')
                    if 'date_ended' in self.fields:
                        self.fields.remove('date_ended')
                if model not in allopurinol_model:
                    if 'de_sensitized' in self.fields:
                        self.fields.remove('de_sensitized')
                if model not in injection_models:
                    if 'as_injection' in self.fields:
                        self.fields.remove('as_injection')
            else:
                model = self.get_queryset().model
                if model not in prn_models:
                    if 'prn' in self.fields:
                        self.fields.remove('prn')
                    if 'date_started' in self.fields:
                        self.fields.remove('date_started')
                    if 'date_ended' in self.fields:
                        self.fields.remove('date_ended')
                if model not in allopurinol_model:
                    if 'de_sensitized' in self.fields:
                        self.fields.remove('de_sensitized')
                if model not in injection_models:
                    if 'as_injection' in self.fields:
                        self.fields.remove('as_injection')
            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )
            return modelform_factory(model, fields=self.fields)

    def get_template_names(self):
        template = "treatment/treatment_form.html"
        return template

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TreatmentUpdate, self).get_context_data(**kwargs)
        context.update({
            'treatment': self.kwargs['treatment'],
        })
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        model = apps.get_model('treatment', model_name=self.kwargs['treatment'])
        try:
            queryset = model.objects.filter(user=self.request.user, pk=pk)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(TreatmentUpdate, self).get_object(queryset=queryset)
        return obj
