from goutdotcom.flare.forms import FlareForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit

from .models import Flare
from ..lab.models import Urate
from .forms import FlareForm
from ..lab.forms import UrateForm
from ..treatment.models import Colchicine, Ibuprofen, Celecoxib, Meloxicam, Naproxen, Prednisone, Methylprednisolone

# Create your views here.
class IndexView(LoginRequiredMixin, ListView):
    template_name = 'flare/index.html'
    model = Flare

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'flare_list': Flare.objects.filter(user=self.request.user),
            'methylprednisolone_inj_list': Methylprednisolone.objects.filter(user=self.request.user),
            'colchicine_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=False),
            'ibuprofen_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=False),
            'celecoxib_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=False),
            'meloxicam_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=False),
            'naproxen_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=False),
            'prednisone_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=False),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

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
    fields = ['location', 'treatment', 'colchicine', 'ibuprofen', 'naproxen', 'celecoxib', 'meloxicam', 'prednisone', 'methylprednisolone', 'duration', 'urate']
    template_name = 'flare/flare_update.html'
    success_url = reverse_lazy('flare:index')

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
def FlareUrateUpdate(request, id):
    context = {}
    flare_for_flare = get_object_or_404(Flare, id=id)
    uric_acid_for_flare = get_object_or_404(Urate, pk=flare_for_flare.urate.pk)
    
    if request.method == "POST":
        flare_form = FlareForm(request.POST, instance=flare_for_flare)
        urate_form = UrateForm(request.POST, instance=uric_acid_for_flare)
        context["flare_form"] = flare_form
        context["urate_form"] = urate_form

        if flare_form.is_valid() and urate_form.is_valid():
            urate_for_flare = urate_form
            urate_for_flare.save()
            flare = flare_form.save(commit=False)
            flare.urate = urate_for_flare
            flare.user = request.user
            id=flare.id
            flare.save()
            return HttpResponseRedirect("/"+id)

    else:
        flare_form = FlareForm(request.POST, instance=flare_for_flare)
        urate_form = UrateForm(request.POST, instance=uric_acid_for_flare)
        context["flare_form"] = flare_form
        context["urate_form"] = urate_form

    return render(request, 'flare/flareurate_update.html', context)
    #return HttpResponseRedirect(reverse('flare:flareurateupdate', kwargs={'pk': flare_for_flare.pk}))

@login_required
def FlareUrateCreate(request):
    if request.method == "POST":
        flare_form = FlareForm(request.POST, instance=Flare())
        urate_form = UrateForm(request.POST, instance=Urate())
        if flare_form.is_valid() and urate_form.is_valid():
            urate_for_flare = urate_form.save(commit=False)
            urate_for_flare.user=request.user
            urate_for_flare.save()
            flare=flare_form.save(commit=False)
            flare.urate = urate_for_flare
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
