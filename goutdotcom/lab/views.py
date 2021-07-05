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

class LabCreate(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        self.object = None
        self.lab = self.kwargs['lab']
        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        """Return the form class to use in this view."""
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            return self.form_class
        else:
            if self.lab is not None:
                # If a model has been explicitly provided, use it
                model = apps.get_model('lab', model_name=self.lab)
            elif getattr(self, 'object', None) is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
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

class UrateDetail(LoginRequiredMixin, DetailView):
    model = Urate

class UrateList(LoginRequiredMixin, ListView):
    model = Urate
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'urate_list': Urate.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class UrateUpdate(LoginRequiredMixin, UpdateView):
    model = Urate
    fields = ['value', 'date_drawn',]
    template_name = 'lab/urate_update.html'

class ALTDetail(LoginRequiredMixin, DetailView):
    model = ALT

class ALTList(LoginRequiredMixin, ListView):
    model = ALT
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'ALT_list': ALT.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class ALTUpdate(LoginRequiredMixin, UpdateView):
    model = ALT
    fields = ['value', 'date_drawn']
    template_name = 'lab/ALT_update.html'

class ASTDetail(LoginRequiredMixin, DetailView):
    model = AST

class ASTList(LoginRequiredMixin, ListView):
    model = AST
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'AST_list': AST.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class ASTUpdate(LoginRequiredMixin, UpdateView):
    model = AST
    fields = ['value', 'date_drawn']
    template_name = 'lab/AST_update.html'

class PlateletDetail(LoginRequiredMixin, DetailView):
    model = Platelet

class PlateletList(LoginRequiredMixin, ListView):
    model = Platelet
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'platelet_list': Platelet.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class PlateletUpdate(LoginRequiredMixin, UpdateView):
    model = Platelet
    fields = ['value', 'date_drawn']
    template_name = 'lab/platelet_update.html'

class WBCDetail(LoginRequiredMixin, DetailView):
    model = WBC

class WBCList(LoginRequiredMixin, ListView):
    model = WBC
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'WBC_list': WBC.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class WBCUpdate(LoginRequiredMixin, UpdateView):
    model = WBC
    fields = ['value', 'date_drawn']
    template_name = 'lab/WBC_update.html'

class HemoglobinDetail(LoginRequiredMixin, DetailView):
    model = Hemoglobin

class HemoglobinList(LoginRequiredMixin, ListView):
    model = Hemoglobin
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'hemoglobin_list': Hemoglobin.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class HemoglobinUpdate(LoginRequiredMixin, UpdateView):
    model = Hemoglobin
    fields = ['value', 'date_drawn']
    template_name = 'lab/hemoglobin_update.html'

class CreatinineDetail(LoginRequiredMixin, DetailView):
    model = Creatinine

class CreatinineList(LoginRequiredMixin, ListView):
    model = Creatinine
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'creatinine_list': Creatinine.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class CreatinineUpdate(LoginRequiredMixin, UpdateView):
    model = Creatinine
    fields = ['value', 'date_drawn']
    template_name = 'lab/creatinine_update.html'
