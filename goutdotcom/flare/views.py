from goutdotcom.flare.forms import FlareForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Flare
from ..lab.models import Urate
from .forms import FlareForm
from ..lab.forms import UrateForm

# Create your views here.
def index(request):
    return render(request, 'flare/index.html')

class FlareCreate(LoginRequiredMixin, CreateView):
    model = Flare
    form_class = FlareForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FlareDetail(LoginRequiredMixin, DetailView):
    model = Flare

class FlareUpdate(LoginRequiredMixin, UpdateView):
    model = Flare
    fields = ['location', 'treatment', 'colchicine', 'ibuprofen', 'naproxen', 'celecoxib', 'meloxicam', 'prednisone', 'methylprednisolone', 'duration', 'urate_draw', 'urate']
    template_name = 'flare/flare_update.html'

@login_required
def Flare2Create(request):
    if request.method == "POST":
        form = FlareForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form = form.save()
    else:
        form = FlareForm()
    return render(request, "flare/flare2create.html", {'form':form,})

@login_required
def FlareUrateCreate(request):
    if request.method == "POST":
        flare_form = FlareForm(request.POST)
        urate_form = UrateForm(request.POST)
        if flare_form.is_valid() and urate_form.is_valid():
            urate=urate_form
            urate_new = Urate.objects.create(uric_acid=urate.instance.uric_acid, user=request.user)
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
    return render(request, "flare/flare_urate_form.html", context)
