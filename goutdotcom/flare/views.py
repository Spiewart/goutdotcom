from goutdotcom.flare.forms import FlareForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit

from .models import Flare
from ..lab.models import Urate
from .forms import FlareForm
from ..lab.forms import UrateForm

# Create your views here.
def index(request):
    return render(request, 'flare/index.html')

class FlareCreate(LoginRequiredMixin, CreateView):
    model = Flare
    fields = ['location', 'treatment', 'colchicine', 'ibuprofen', 'naproxen', 'celecoxib', 'meloxicam', 'prednisone', 'methylprednisolone', 'duration', 'urate']
    template_name = 'flare/flare_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FlareDetail(LoginRequiredMixin, DetailView):
    model = Flare

class FlareUpdate(LoginRequiredMixin, UpdateView):
    model = Flare
    fields = ['location', 'treatment', 'colchicine', 'ibuprofen', 'naproxen', 'celecoxib', 'meloxicam', 'prednisone', 'methylprednisolone', 'duration', 'urate_draw', 'urate']
    template_name = 'flare/flare_update.html'

class FlareList(LoginRequiredMixin, ListView):
    model = Flare

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'flare_list': Flare.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

@login_required
def FlareUrateCreate(request):
    if request.method == "POST":
        flare_form = FlareForm(request.POST)
        urate_form = UrateForm(request.POST)
        if flare_form.is_valid() and urate_form.is_valid():
            urate=urate_form
            urate_new = Urate.objects.create(uric_acid=urate.instance.uric_acid, user=request.user)
            urate_new.save()
            flare=flare_form.save(commit=False)
            flare.urate=urate_new
            flare.user=request.user
            flare.save()
            return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))
    else:
        flare_form = FlareForm()
        flare_form.user = request.user
        urate_form = UrateForm()
        urate_form.user = request.user

    context = {'urate_form':urate_form, 'flare_form':flare_form,}
    return render(request, "flare/flareurate_form.html", context)

def Landing(request):
    return render(request, 'flare/landing.html')
