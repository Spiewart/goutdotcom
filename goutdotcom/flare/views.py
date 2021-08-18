from goutdotcom.flare.forms import FlareForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .models import Flare
from ..lab.models import Urate
from .forms import FlareForm
from ..lab.forms import UrateForm
from ..treatment.forms import ColchicineForm, IbuprofenForm, NaproxenForm, CelecoxibForm, MeloxicamForm, OthertreatForm, PrednisoneForm, MethylprednisoloneForm, ColchicineFlareForm, IbuprofenFlareForm, NaproxenFlareForm, CelecoxibFlareForm, MeloxicamFlareForm, PrednisoneFlareForm, MethylprednisoloneFlareForm, TinctureoftimeFlareForm, OthertreatFlareForm, TinctureoftimeForm
from ..treatment.models import Colchicine, Ibuprofen, Celecoxib, Meloxicam, Naproxen, Prednisone, Methylprednisolone, Tinctureoftime, Othertreat

# Create your views here.
class IndexView(LoginRequiredMixin, ListView):
    template_name = 'flare/index.html'
    model = Flare

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'flare_list': Flare.objects.filter(user=self.request.user).order_by('-created')[:5],
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

class FlareDetail(LoginRequiredMixin, DetailView):
    model = Flare

class FlareUpdate(LoginRequiredMixin, UpdateView):
    model = Flare
    fields = ['location', 'treatment', 'colchicine', 'ibuprofen', 'naproxen', 'celecoxib', 'meloxicam', 'prednisone', 'methylprednisolone', 'duration', 'urate']
    template_name = 'flare/flare_update.html'
    success_url = reverse_lazy('flare:index')

class FlareList(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Flare

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'flare_list': Flare.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class FlareCreate(LoginRequiredMixin, CreateView):
    model = Flare
    form_class = FlareForm
    urate_form_class = UrateForm
    colchicine_form_class = ColchicineFlareForm
    ibuprofen_form_class = IbuprofenFlareForm
    naproxen_form_class = NaproxenFlareForm
    celecoxib_form_class = CelecoxibFlareForm
    meloxicam_form_class = MeloxicamFlareForm
    prednisone_form_class = PrednisoneFlareForm
    methylprednisolone_form_class = MethylprednisoloneFlareForm
    tinctureoftime_form_class = TinctureoftimeFlareForm
    othertreat_form_class = OthertreatFlareForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FlareCreate, self).get_context_data(**kwargs)
        context.update({
            'user': self.request.user
        })
        if 'urate_form' not in context:
            context['urate_form'] = self.urate_form_class(self.request.GET)
        if 'colchicine_form' not in context:
            context['colchicine_form'] = self.colchicine_form_class(self.request.GET)
        if 'ibuprofen_form' not in context:
            context['ibuprofen_form'] = self.ibuprofen_form_class(self.request.GET)
        if 'naproxen_form' not in context:
            context['naproxen_form'] = self.naproxen_form_class(self.request.GET)
        if 'celecoxib_form' not in context:
            context['celecoxib_form'] = self.celecoxib_form_class(self.request.GET)
        if 'meloxicam_form' not in context:
            context['meloxicam_form'] = self.meloxicam_form_class(self.request.GET)
        if 'prednisone_form' not in context:
            context['prednisone_form'] = self.prednisone_form_class(self.request.GET)
        if 'methylprednisolone_form' not in context:
            context['methylprednisolone_form'] = self.methylprednisolone_form_class(self.request.GET)
        if 'tinctureoftime_form' not in context:
            context['tinctureoftime_form'] = self.tinctureoftime_form_class(self.request.GET)
        if 'othertreat_form' not in context:
            context['othertreat_form'] = self.othertreat_form_class(self.request.GET)
        return context

    def get_object(self):
        object = self.model
        return object

    def post(self, request):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=Flare())
        urate_form = self.urate_form_class(request.POST, instance=Urate())
        colchicine_form = self.colchicine_form_class(request.POST, instance=Colchicine())
        ibuprofen_form = self.ibuprofen_form_class(request.POST, instance=Ibuprofen())
        naproxen_form = self.naproxen_form_class(request.POST, instance=Naproxen())
        celecoxib_form = self.celecoxib_form_class(request.POST, instance=Celecoxib())
        meloxicam_form = self.meloxicam_form_class(request.POST, instance=Meloxicam())
        prednisone_form = self.prednisone_form_class(request.POST, instance=Prednisone())
        methylprednisolone_form = self.methylprednisolone_form_class(request.POST, instance=Methylprednisolone())
        tinctureoftime_form = self.tinctureoftime_form_class(request.POST, instance=Tinctureoftime())
        othertreat_form = self.othertreat_form_class(request.POST, instance=Othertreat())

        if form.is_valid():
            flare_data = form.save(commit=False)
            flare_data.user = request.user
            if urate_form.is_valid():
                urate_data = urate_form.save(commit=False)
                urate_data.user = request.user
                urate_data.save()
                flare_data.urate = urate_data
            if "Colcrys" in flare_data.treatment and colchicine_form.is_valid():
                colchicine_data = colchicine_form.save(commit=False)
                colchicine_data.user = request.user
                colchicine_data.save()
                flare_data.colchicine = colchicine_data
            if "Advil" in flare_data.treatment and ibuprofen_form.is_valid():
                ibuprofen_data = ibuprofen_form.save(commit=False)
                ibuprofen_data.user = request.user
                ibuprofen_data.save()
                flare_data.ibuprofen = ibuprofen_data
            if "Aleve" in flare_data.treatment and naproxen_form.is_valid():
                naproxen_data = naproxen_form.save(commit=False)
                naproxen_data.user = request.user
                naproxen_data.save()
                flare_data.naproxen = naproxen_data
            if "Celebrex" in flare_data.treatment and celecoxib_form.is_valid():
                celecoxib_data = celecoxib_form.save(commit=False)
                celecoxib_data.user = request.user
                celecoxib_data.save()
                flare_data.celecoxib = celecoxib_data
            if "Mobic" in flare_data.treatment and meloxicam_form.is_valid():
                meloxicam_data = meloxicam_form.save(commit=False)
                meloxicam_data.user = request.user
                meloxicam_data.save()
                flare_data.meloxicam = meloxicam_data
            if "Prednisone" in flare_data.treatment and prednisone_form.is_valid():
                prednisone_data = prednisone_form.save(commit=False)
                prednisone_data.user = request.user
                prednisone_data.save()
                flare_data.prednisone = prednisone_data
            if "Methylprednisolone" in flare_data.treatment and methylprednisolone_form.is_valid():
                methylprednisolone_data = methylprednisolone_form.save(commit=False)
                methylprednisolone_data.user = request.user
                methylprednisolone_data.save()
                flare_data.methylprednisolone = methylprednisolone_data
            if "Tincture of time" in flare_data.treatment and tinctureoftime_form.is_valid():
                tinctureoftime_data = tinctureoftime_form.save(commit=False)
                tinctureoftime_data.user = request.user
                tinctureoftime_data.save()
                flare_data.tinctureoftime = tinctureoftime_data
            if "Other treatment" in flare_data.treatment and othertreat_form.is_valid():
                othertreat_data = othertreat_form.save(commit=False)
                othertreat_data.user = request.user
                othertreat_data.save()
                flare_data.othertreat = othertreat_data
            flare_data.save()
            return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk': flare_data.pk}))
        else:
            return self.render_to_response(
                self.get_context_data(form=form, urate_form=urate_form, colchicine_form=colchicine_form, ibuprofen_form=ibuprofen_form, naproxen_form=naproxen_form, celecoxib_form=celecoxib_form, meloxicam_form=meloxicam_form, prednisone_form=prednisone_form, methylprednisolone_form=methylprednisolone_form, tinctureoftime_form=tinctureoftime_form, othertreat_form=othertreat_form))

