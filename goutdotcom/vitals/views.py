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
            'weight_list': Weight.objects.filter(user=self.request.user).order_by('-date_recorded')[:1],
            'height_list': Height.objects.filter(user=self.request.user).order_by('-date_recorded')[:1],
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
