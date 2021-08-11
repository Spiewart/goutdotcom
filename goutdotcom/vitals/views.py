from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import modelform_factory
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from .models import Weight, Height

# Create your views here.
class IndexView(LoginRequiredMixin, ListView):
    template_name = 'vitals/index.html'
    model = Weight

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'weight_list': Weight.objects.filter(user=self.request.user).order_by('-date_recorded')[:5],
            'height_list': Height.objects.filter(user=self.request.user).order_by('-date_recorded')[:5],
        })
        return context


class VitalCreate(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        self.object = None
        self.vital = self.kwargs['vital']
        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        self.vital = self.kwargs['vital']
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            return self.form_class
        else:
            if self.vital is not None:
                # Fetch model from URL 'vital' parameter
                model = apps.get_model('vitals', model_name=self.vital)
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

    def get_template_names(self):
        template = "vitals/vital_form.html"
        return template

    fields = ['value',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VitalCreate, self).get_context_data(**kwargs)
        context.update({
            'vital': self.kwargs['vital'],
        })
        return context

class VitalDetail(LoginRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        self.model = apps.get_model('vitals', model_name=self.kwargs['vital'])
        vital = get_object_or_404(self.model, pk=self.kwargs['pk'], user=self.request.user)
        return vital

    def get_template_names(self):
        template = "vitals/vital_detail.html"
        return template

class VitalList(LoginRequiredMixin, ListView):
    paginate_by=5

    def get_queryset(self):
        self.model = apps.get_model('vitals', model_name=self.kwargs['vital'])
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
        template = "vitals/vital_list.html"
        return template

    def get_context_data(self, **kwargs):
        self.model = apps.get_model('vitals', model_name=self.kwargs['vital'])
        context = super(VitalList, self).get_context_data(**kwargs)
        context.update({
            'vital': self.kwargs['vital'],
        })
        return context

class VitalUpdate(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        self.vital = self.kwargs['vital']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VitalUpdate, self).get_context_data(**kwargs)
        context.update({
            'vital': self.kwargs['vital'],
        })
        return context

    def get_form_class(self):
        self.vital = self.kwargs['vital']
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            return self.form_class
        else:
            if self.vital is not None:
                # Fetch model from URL 'vital' parameter
                model = apps.get_model('vitals', model_name=self.vital)
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

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        model = apps.get_model('vitals', model_name=self.kwargs['vital'])
        try:
            queryset = model.objects.filter(user=self.request.user, pk=pk)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")

        obj = super(VitalUpdate, self).get_object(queryset=queryset)
        return obj

    def get_template_names(self):
        template = "vitals/vital_form.html"
        return template

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    fields = ['value',]


