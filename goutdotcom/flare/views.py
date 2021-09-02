from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import NullBooleanField
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from .models import Flare
from ..lab.models import Urate
from .forms import FlareForm
from ..lab.forms import UrateFlareForm
from ..treatment.forms import ColchicineFlareForm, IbuprofenFlareForm, NaproxenFlareForm, CelecoxibFlareForm, MeloxicamFlareForm, PrednisoneFlareForm, MethylprednisoloneFlareForm, TinctureoftimeFlareForm, OthertreatFlareForm
from ..treatment.models import Colchicine, Ibuprofen, Celecoxib, Meloxicam, Naproxen, Prednisone, Methylprednisolone, Tinctureoftime, Othertreat

# Create your views here.

class AboutFlares(TemplateView):
    template_name = "flare/about.html"

class FlareDetail(LoginRequiredMixin, DetailView):
    model = Flare

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
    urate_form_class = UrateFlareForm
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

        if form.is_valid():
            flare_data = form.save(commit=False)
            flare_data.user = request.user
            if "Urate" in flare_data.labs:
                urate_form = self.urate_form_class(request.POST, instance=Urate())
                if urate_form.is_valid():
                    urate_data = urate_form.save(commit=False)
                    urate_data.user = request.user
                    urate_data.save()
                    flare_data.urate = urate_data
            if "Colcrys" in flare_data.treatment:
                colchicine_form = self.colchicine_form_class(request.POST, instance=Colchicine())
                if colchicine_form.is_valid():
                    colchicine_data = colchicine_form.save(commit=False)
                    colchicine_data.user = request.user
                    colchicine_data.save()
                    flare_data.colchicine = colchicine_data
            if "Advil" in flare_data.treatment:
                ibuprofen_form = self.ibuprofen_form_class(request.POST, instance=Ibuprofen())
                if ibuprofen_form.is_valid():
                    ibuprofen_data = ibuprofen_form.save(commit=False)
                    ibuprofen_data.user = request.user
                    ibuprofen_data.save()
                    flare_data.ibuprofen = ibuprofen_data
            if "Aleve" in flare_data.treatment:
                naproxen_form = self.naproxen_form_class(request.POST, instance=Naproxen())
                if naproxen_form.is_valid():
                    naproxen_data = naproxen_form.save(commit=False)
                    naproxen_data.user = request.user
                    naproxen_data.save()
                    flare_data.naproxen = naproxen_data
            if "Celebrex" in flare_data.treatment:
                celecoxib_form = self.celecoxib_form_class(request.POST, instance=Celecoxib())
                if celecoxib_form.is_valid():
                    celecoxib_data = celecoxib_form.save(commit=False)
                    celecoxib_data.user = request.user
                    celecoxib_data.save()
                    flare_data.celecoxib = celecoxib_data
            if "Mobic" in flare_data.treatment:
                meloxicam_form = self.meloxicam_form_class(request.POST, instance=Meloxicam())
                if meloxicam_form.is_valid():
                    meloxicam_data = meloxicam_form.save(commit=False)
                    meloxicam_data.user = request.user
                    meloxicam_data.save()
                    flare_data.meloxicam = meloxicam_data
            if "Prednisone" in flare_data.treatment:
                prednisone_form = self.prednisone_form_class(request.POST, instance=Prednisone())
                if prednisone_form.is_valid():
                    prednisone_data = prednisone_form.save(commit=False)
                    prednisone_data.user = request.user
                    prednisone_data.save()
                    flare_data.prednisone = prednisone_data
            if "Methylprednisolone" in flare_data.treatment:
                methylprednisolone_form = self.methylprednisolone_form_class(
                    request.POST, instance=Methylprednisolone())
                if methylprednisolone_form.is_valid():
                    methylprednisolone_data = methylprednisolone_form.save(commit=False)
                    methylprednisolone_data.user = request.user
                    methylprednisolone_data.save()
                    flare_data.methylprednisolone = methylprednisolone_data
            if "Tincture of time" in flare_data.treatment:
                tinctureoftime_form = self.tinctureoftime_form_class(request.POST, instance=Tinctureoftime())
                if tinctureoftime_form.is_valid():
                    tinctureoftime_data = tinctureoftime_form.save(commit=False)
                    tinctureoftime_data.user = request.user
                    tinctureoftime_data.save()
                    flare_data.tinctureoftime = tinctureoftime_data
            if "Other treatment" in flare_data.treatment:
                othertreat_form = self.othertreat_form_class(request.POST, instance=Othertreat())
                if othertreat_form.is_valid():
                    othertreat_data = othertreat_form.save(commit=False)
                    othertreat_data.user = request.user
                    othertreat_data.save()
                    flare_data.othertreat = othertreat_data
            flare_data.save()
            return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk': flare_data.pk}))
        else:
            return self.render_to_response(
                self.get_context_data(form=form,
                                      urate_form=self.urate_form_class(request.POST, instance=Urate()),
                                      colchicine_form=self.colchicine_form_class(request.POST, instance=Othertreat()),
                                      ibuprofen_form=self.ibuprofen_form_class(request.POST, instance=Othertreat()),
                                      naproxen_form=self.naproxen_form_class(request.POST, instance=Othertreat()),
                                      celecoxib_form=self.celecoxib_form_class(request.POST, instance=Othertreat()),
                                      meloxicam_form=self.meloxicam_form_class(request.POST, instance=Othertreat()),
                                      prednisone_form=self.prednisone_form_class(request.POST, instance=Othertreat()),
                                      methylprednisolone_form=self.methylprednisolone_form_class(request.POST, instance=Othertreat()),
                                      tinctureoftime_form=self.tinctureoftime_form_class(request.POST, instance=Othertreat()),
                                      othertreat_form=self.othertreat_form_class(request.POST, instance=Othertreat())
                                      )
                )


class FlareUpdate(LoginRequiredMixin, UpdateView):
    model = Flare

    form_class = FlareForm
    urate_form_class = UrateFlareForm
    colchicine_form_class = ColchicineFlareForm
    ibuprofen_form_class = IbuprofenFlareForm
    naproxen_form_class = NaproxenFlareForm
    celecoxib_form_class = CelecoxibFlareForm
    meloxicam_form_class = MeloxicamFlareForm
    prednisone_form_class = PrednisoneFlareForm
    methylprednisolone_form_class = MethylprednisoloneFlareForm
    tinctureoftime_form_class = TinctureoftimeFlareForm
    othertreat_form_class = OthertreatFlareForm

    def get_context_data(self, **kwargs):
        context = super(FlareUpdate, self).get_context_data(**kwargs)
        context.update({
            'user': self.request.user
        })
        if self.request.POST:
            context['urate_form'] = self.urate_form_class(
                self.request.POST, instance=self.object.urate)
            context['colchicine_form'] = self.colchicine_form_class(
                self.request.POST, instance=self.object.colchicine)
            context['ibuprofen_form'] = self.ibuprofen_form_class(
                self.request.POST, instance=self.object.ibuprofen)
            context['naproxen_form'] = self.naproxen_form_class(
                self.request.POST, instance=self.object.naproxen)
            context['celecoxib_form'] = self.celecoxib_form_class(
                self.request.POST, instance=self.object.celecoxib)
            context['meloxicam_form'] = self.meloxicam_form_class(
                self.request.POST, instance=self.object.meloxicam)
            context['prednisone_form'] = self.prednisone_form_class(
                self.request.POST, instance=self.object.prednisone)
            context['methylprednisolone_form'] = self.methylprednisolone_form_class(
                self.request.POST, instance=self.object.methylprednisolone)
            context['tinctureoftime_form'] = self.tinctureoftime_form_class(
                self.request.POST, instance=self.object.tinctureoftime)
            context['othertreat_Form'] = self.othertreat_form_class(
                self.request.POST, instance=self.object.othertreat)
        else:
            context['urate_form'] = self.urate_form_class(instance=self.object.urate)
            context['colchicine_form'] = self.colchicine_form_class(instance=self.object.colchicine)
            context['ibuprofen_form'] = self.ibuprofen_form_class(instance=self.object.ibuprofen)
            context['naproxen_form'] = self.naproxen_form_class(instance=self.object.naproxen)
            context['celecoxib_form'] = self.celecoxib_form_class(instance=self.object.celecoxib)
            context['meloxicam_form'] = self.meloxicam_form_class(instance=self.object.meloxicam)
            context['prednisone_form'] = self.prednisone_form_class(instance=self.object.prednisone)
            context['methylprednisolone_form'] = self.methylprednisolone_form_class(instance=self.object.methylprednisolone)
            context['tinctureoftime_form'] = self.tinctureoftime_form_class(instance=self.object.tinctureoftime)
            context['othertreat_form'] = self.othertreat_form_class(instance=self.object.othertreat)
        return context

    def get_object(self, queryset=None):
        try:
            queryset = self.model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(FlareUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            flare_data = form.save(commit=False)
            flare_data.user = request.user
            if "Urate" in flare_data.labs:
                urate_form = self.urate_form_class(request.POST, instance=self.object.urate)
                if urate_form.is_valid():
                    urate_data = urate_form.save(commit=False)
                    urate_data.user = request.user
                    urate_data.save()
                    flare_data.urate = urate_data
            elif "Urate" not in flare_data.labs:
                if self.object.urate:
                    self.object.urate.delete()
                    flare_data.urate = None
            if "Colcrys" in flare_data.treatment:
                colchicine_form = self.colchicine_form_class(request.POST, instance=self.object.colchicine)
                if colchicine_form.is_valid():
                    colchicine_data = colchicine_form.save(commit=False)
                    colchicine_data.user = request.user
                    colchicine_data.save()
                    flare_data.colchicine = colchicine_data
            elif "Colcrys" not in flare_data.treatment:
                if self.object.colchicine:
                    self.object.colchicine.delete()
                    flare_data.colchicine = None
            if "Advil" in flare_data.treatment:
                ibuprofen_form = self.ibuprofen_form_class(request.POST, instance=self.object.ibuprofen)
                if ibuprofen_form.is_valid():
                    ibuprofen_data = ibuprofen_form.save(commit=False)
                    ibuprofen_data.user = request.user
                    ibuprofen_data.save()
                    flare_data.ibuprofen = ibuprofen_data
            elif "Advil" not in flare_data.treatment:
                if self.object.ibuprofen:
                    self.object.ibuprofen.delete()
                    flare_data.ibuprofen = None
            if "Aleve" in flare_data.treatment:
                naproxen_form = self.naproxen_form_class(request.POST, instance=self.object.naproxen)
                if naproxen_form.is_valid():
                    naproxen_data = naproxen_form.save(commit=False)
                    naproxen_data.user = request.user
                    naproxen_data.save()
                    flare_data.naproxen = naproxen_data
            elif "Aleve" not in flare_data.treatment:
                if self.object.naproxen:
                    self.object.naproxen.delete()
                    flare_data.naproxen = None
            if "Celebrex" in flare_data.treatment:
                celecoxib_form = self.celecoxib_form_class(request.POST, instance=self.object.celecoxib)
                if celecoxib_form.is_valid():
                    celecoxib_data = celecoxib_form.save(commit=False)
                    celecoxib_data.user = request.user
                    celecoxib_data.save()
                    flare_data.celecoxib = celecoxib_data
            elif "Celebrex" not in flare_data.treatment:
                if self.object.celecoxib:
                    self.object.celecoxib.delete()
                    flare_data.celecoxib = None
            if "Mobic" in flare_data.treatment:
                meloxicam_form = self.meloxicam_form_class(request.POST, instance=self.object.meloxicam)
                if meloxicam_form.is_valid():
                    meloxicam_data = meloxicam_form.save(commit=False)
                    meloxicam_data.user = request.user
                    meloxicam_data.save()
                    flare_data.meloxicam = meloxicam_data
            elif "Mobic" not in flare_data.treatment:
                if self.object.meloxicam:
                    self.object.meloxicam.delete()
                    flare_data.meloxicam = None
            if "Prednisone" in flare_data.treatment:
                prednisone_form = self.prednisone_form_class(request.POST, instance=self.object.prednisone)
                if prednisone_form.is_valid():
                    prednisone_data = prednisone_form.save(commit=False)
                    prednisone_data.user = request.user
                    prednisone_data.save()
                    flare_data.prednisone = prednisone_data
            elif "Prednisone" not in flare_data.treatment:
                if self.object.prednisone:
                    self.object.prednisone.delete()
                    flare_data.prednisone = None
            if "Methylprednisolone" in flare_data.treatment:
                methylprednisolone_form = self.methylprednisolone_form_class(
                    request.POST, instance=self.object.methylprednisolone)
                if methylprednisolone_form.is_valid():
                    methylprednisolone_data = methylprednisolone_form.save(commit=False)
                    methylprednisolone_data.user = request.user
                    methylprednisolone_data.save()
                    flare_data.methylprednisolone = methylprednisolone_data
            elif "Methylprednisolone" not in flare_data.treatment:
                if self.object.methylprednisolone:
                    self.object.methylprednisolone.delete()
                    flare_data.methylprednisolone = None
            if "Tincture of time" in flare_data.treatment:
                tinctureoftime_form = self.tinctureoftime_form_class(request.POST, instance=self.object.tinctureoftime)
                if tinctureoftime_form.is_valid():
                    tinctureoftime_data = tinctureoftime_form.save(commit=False)
                    tinctureoftime_data.user = request.user
                    tinctureoftime_data.save()
                    flare_data.tinctureoftime = tinctureoftime_data
                elif "Tincture of time" not in flare_data.treatment:
                    if self.object.tinctureoftime:
                        self.object.tinctureoftime.delete()
                        flare_data.tinctureoftime = None
            if "Other treatment" in flare_data.treatment:
                othertreat_form = self.othertreat_form_class(request.POST, instance=self.object.othertreat)
                if othertreat_form.is_valid():
                    othertreat_data = othertreat_form.save(commit=False)
                    othertreat_data.user = request.user
                    othertreat_data.save()
                    flare_data.othertreat = othertreat_data
                elif "Other treatment" not in flare_data.treatment:
                    if self.object.othertreat:
                        self.object.othertreat.delete()
                        flare_data.othertreat = None
            flare_data.save()
            return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk': flare_data.pk}))
        else:
            return self.render_to_response(
                self.get_context_data(form=form,
                                    urate_form=self.urate_form_class(request.POST, instance=Urate()),
                                    colchicine_form=self.colchicine_form_class(request.POST, instance=Othertreat()),
                                    ibuprofen_form=self.ibuprofen_form_class(request.POST, instance=Othertreat()),
                                    naproxen_form=self.naproxen_form_class(request.POST, instance=Othertreat()),
                                    celecoxib_form=self.celecoxib_form_class(request.POST, instance=Othertreat()),
                                    meloxicam_form=self.meloxicam_form_class(request.POST, instance=Othertreat()),
                                    prednisone_form=self.prednisone_form_class(request.POST, instance=Othertreat()),
                                    methylprednisolone_form=self.methylprednisolone_form_class(request.POST, instance=Othertreat()),
                                    tinctureoftime_form=self.tinctureoftime_form_class(request.POST, instance=Othertreat()),
                                    othertreat_form=self.othertreat_form_class(request.POST, instance=Othertreat())
                                    )
                )

