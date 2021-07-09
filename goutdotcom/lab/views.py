from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory
from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from .models import ALT, AST, Creatinine, Hemoglobin, Lab, Platelet, Urate, WBC

# Create your views here.
class LabAbout(TemplateView):
    def get_template_names(self, **kwargs):
        kwargs = self.kwargs
        lab = kwargs.get('lab')
        template = "lab/" + str(lab) + "_about.html"
        return template

    def get_context_data(self, **kwargs):
        context = super(LabAbout, self).get_context_data(**kwargs)
        context.update({
            'lab': self.kwargs['lab'],
        })
        return context

class LabCreate(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        self.object = None
        self.lab = self.kwargs['lab']
        return super().get(request, *args, **kwargs)

    def get_form_class(self, **kwargs):
        self.lab = self.kwargs['lab']
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            return self.form_class
        else:
            if self.lab is not None:
                # Fetch model from URL 'lab' parameter
                model = apps.get_model('lab', model_name=self.lab)
            elif getattr(self, 'object', None) is not None:
                model = self.object.__class__
            else:
                model = self.get_queryset().model
            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )
            return modelform_factory(model, fields=self.fields)

    def get_template_names(self, **kwargs):
        kwargs = self.kwargs
        lab = kwargs.get('lab')
        template = "lab/" + str(lab) + "_form.html"
        return template 

    fields = ['value', 'date_drawn',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LabCreate, self).get_context_data(**kwargs)
        context.update({
            'lab': self.kwargs['lab'],
        })
        return context

class LabDetail(LoginRequiredMixin, DetailView):
    def get_queryset(self, **kwargs):
        self.model = apps.get_model('lab', model_name=self.kwargs['lab'])
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset.all()

    def get_template_names(self, **kwargs):
        kwargs = self.kwargs
        lab = kwargs.get('lab')
        template = "lab/lab_detail_base.html"
        return template 

class LabList(LoginRequiredMixin, ListView):
    paginate_by=5

    def get_queryset(self):
        self.model = apps.get_model('lab', model_name=self.kwargs['lab'])
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

    def get_template_names(self, **kwargs):
        kwargs = self.kwargs
        lab = kwargs.get('lab')
        template = "lab/" + str(lab) + "_list.html"
        return template 

    def get_context_data(self, **kwargs):
        self.model = apps.get_model('lab', model_name=self.kwargs['lab'])
        context = super(LabList, self).get_context_data(**kwargs)
        context.update({
            'lab': self.kwargs['lab'],
        })
        return context

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'lab/index.html'
    model = Urate

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'urate_list': Urate.objects.filter(user=self.request.user).order_by('-created')[:3],
            'ALT_list': ALT.objects.filter(user=self.request.user).order_by('-created')[:3],
            'AST_list': AST.objects.filter(user=self.request.user).order_by('-created')[:3],
            'platelet_list': Platelet.objects.filter(user=self.request.user).order_by('-created')[:3],
            'WBC_list': WBC.objects.filter(user=self.request.user).order_by('-created')[:3],
            'hemoglobin_list': Hemoglobin.objects.filter(user=self.request.user).order_by('-created')[:3],
            'creatinine_list': Creatinine.objects.filter(user=self.request.user).order_by('-created')[:3],
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class UrateUpdate(LoginRequiredMixin, UpdateView):
    model = Urate
    fields = ['value', 'date_drawn',]
    template_name = 'lab/urate_update.html'

class ALTUpdate(LoginRequiredMixin, UpdateView):
    model = ALT
    fields = ['value', 'date_drawn']
    template_name = 'lab/ALT_update.html'

class ASTUpdate(LoginRequiredMixin, UpdateView):
    model = AST
    fields = ['value', 'date_drawn']
    template_name = 'lab/AST_update.html'

class PlateletUpdate(LoginRequiredMixin, UpdateView):
    model = Platelet
    fields = ['value', 'date_drawn']
    template_name = 'lab/platelet_update.html'

class WBCUpdate(LoginRequiredMixin, UpdateView):
    model = WBC
    fields = ['value', 'date_drawn']
    template_name = 'lab/WBC_update.html'

class HemoglobinUpdate(LoginRequiredMixin, UpdateView):
    model = Hemoglobin
    fields = ['value', 'date_drawn']
    template_name = 'lab/hemoglobin_update.html'

class CreatinineUpdate(LoginRequiredMixin, UpdateView):
    model = Creatinine
    fields = ['value', 'date_drawn']
    template_name = 'lab/creatinine_update.html'
