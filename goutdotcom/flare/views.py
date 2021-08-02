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
from ..treatment.forms import ColchicineForm, IbuprofenForm, NaproxenForm, CelecoxibForm, MeloxicamForm, PrednisoneForm, MethylprednisoloneForm, ColchicineFlareForm, IbuprofenFlareForm, NaproxenFlareForm, CelecoxibFlareForm, MeloxicamFlareForm, PrednisoneFlareForm, MethylprednisoloneFlareForm, TinctureoftimeFlareForm, OthertreatFlareForm
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
def FlareCreate(request):
    if request.method == "POST":
        flare_form = FlareForm(request.POST, instance=Flare())
        urate_form = UrateForm(request.POST, instance=Urate())
        colchicine_form = ColchicineFlareForm(request.POST, instance=Colchicine())
        ibuprofen_form = IbuprofenFlareForm(request.POST, instance=Ibuprofen())
        naproxen_form = NaproxenFlareForm(request.POST, instance=Naproxen())
        celecoxib_form = CelecoxibFlareForm(request.POST, instance=Celecoxib())
        meloxicam_form = MeloxicamFlareForm(request.POST, instance=Meloxicam())
        prednisone_form = PrednisoneFlareForm(request.POST, instance=Prednisone())
        methylprednisolone_form = MethylprednisoloneFlareForm(request.POST, instance=Methylprednisolone())
        tinctureoftime_form = TinctureoftimeFlareForm(request.POST, instance=Tinctureoftime())
        othertreat_form = OthertreatFlareForm(request.POST, instance=Othertreat())

        if flare_form.is_valid():
            flare=flare_form.save(commit=False)
            if flare.treatment == "Colcrys" and urate_form.is_valid() and colchicine_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                colchicine_for_flare = colchicine_form.save(commit=False)
                colchicine_for_flare.user=request.user
                colchicine_for_flare.save()
                flare.urate = urate_for_flare
                flare.colchicine = colchicine_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

            elif flare.treatment == "Advil" and urate_form.is_valid() and ibuprofen_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                ibuprofen_for_flare = ibuprofen_form.save(commit=False)
                ibuprofen_for_flare.user=request.user
                ibuprofen_for_flare.save()
                flare.urate = urate_for_flare
                flare.ibuprofen = ibuprofen_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

            elif flare.treatment == "Aleve" and urate_form.is_valid() and naproxen_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                naproxen_for_flare = naproxen_form.save(commit=False)
                naproxen_for_flare.user=request.user
                naproxen_for_flare.save()
                flare.urate = urate_for_flare
                flare.naproxen = naproxen_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

            elif flare.treatment == "Celebrex" and urate_form.is_valid() and celecoxib_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                celecoxib_for_flare = celecoxib_form.save(commit=False)
                celecoxib_for_flare.user=request.user
                celecoxib_for_flare.save()
                flare.urate = urate_for_flare
                flare.celecoxib = celecoxib_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

            elif flare.treatment == "Mobic" and urate_form.is_valid() and meloxicam_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                meloxicam_for_flare = meloxicam_form.save(commit=False)
                meloxicam_for_flare.user=request.user
                meloxicam_for_flare.save()
                flare.urate = urate_for_flare
                flare.meloxicam = meloxicam_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

            elif flare.treatment == "Pred" and urate_form.is_valid() and prednisone_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                prednisone_for_flare = prednisone_form.save(commit=False)
                prednisone_for_flare.user=request.user
                prednisone_for_flare.save()
                flare.urate = urate_for_flare
                flare.prednisone = prednisone_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

            elif flare.treatment == "Methylpred" and urate_form.is_valid() and methylprednisolone_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                methylprednisolone_for_flare = methylprednisolone_form.save(commit=False)
                methylprednisolone_for_flare.user=request.user
                methylprednisolone_for_flare.save()
                flare.urate = urate_for_flare
                flare.methylprednisolone = methylprednisolone_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

            elif flare.treatment == "Tincture of time" and urate_form.is_valid() and tinctureoftime_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                tinctureoftime_for_flare = methylprednisolone_form.save(commit=False)
                tinctureoftime_for_flare.user=request.user
                tinctureoftime_for_flare.save()
                flare.urate = urate_for_flare
                flare.tinctureoftime = tinctureoftime_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

            elif flare.treatment == "Other treatment" and urate_form.is_valid() and othertreat_form.is_valid():
                urate_for_flare = urate_form.save(commit=False)
                urate_for_flare.user=request.user
                urate_for_flare.save()
                othertreat_for_flare = othertreat_form.save(commit=False)
                othertreat_for_flare.user=request.user
                othertreat_for_flare.save()
                flare.urate = urate_for_flare
                flare.othertreat = othertreat_for_flare
                flare.user=request.user
                flare.save()
                return HttpResponseRedirect(reverse('flare:detail', kwargs={'pk':flare.pk}))

    else:
        flare_form = FlareForm()
        urate_form = UrateForm()
        colchicine_form = ColchicineFlareForm()
        ibuprofen_form = IbuprofenFlareForm()
        naproxen_form = NaproxenFlareForm()
        meloxicam_form = MeloxicamFlareForm()
        celecoxib_form = CelecoxibFlareForm()
        prednisone_form = PrednisoneFlareForm()
        methylprednisolone_form = MethylprednisoloneFlareForm()
        tinctureoftime_form = TinctureoftimeFlareForm()
        othertreat_form = OthertreatFlareForm()

    context = {'urate_form':urate_form, 'flare_form':flare_form, 'colchicine_form':colchicine_form, 'ibuprofen_form':ibuprofen_form, 'naproxen_form':naproxen_form, 'meloxicam_form':meloxicam_form, 'celecoxib_form':celecoxib_form, 'prednisone_form':prednisone_form, 'methylprednisolone_form':methylprednisolone_form, 'tinctureoftime_form':tinctureoftime_form, 'othertreat_form':othertreat_form,}
    return render(request, "flare/flarecreate_form.html", context)

