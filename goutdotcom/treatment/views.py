from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Allopurinol, Colchicine, Febuxostat, Ibuprofen, Celecoxib, Meloxicam, Naproxen, Prednisone, Probenecid, Methylprednisolone, Tinctureoftime, Othertreat


class DashboardView(ListView):
    template_name = 'treatment/dashboard.html'
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'allopurinol_list': Allopurinol.objects.filter(user=self.request.user),
            'febuxostat_list': Febuxostat.objects.filter(user=self.request.user),
            'colchicine_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=False),
            'ibuprofen_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=False),
            'celecoxib_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=False),
            'meloxicam_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=False),
            'naproxen_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=False),
            'prednisone_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=False),
            'probenecid_list': Probenecid.objects.filter(user=self.request.user),
            'methylprednisolone_list': Methylprednisolone.objects.filter(user=self.request.user),
            'colchicine_ppx_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=True),
            'ibuprofen_ppx_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=True),
            'celecoxib_ppx_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=True),
            'meloxicam_ppx_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=True),
            'naproxen_ppx_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=True),
            'prednisone_ppx_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=True),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class IndexView(ListView):
    template_name = 'treatment/index.html'
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'allopurinol_list': Allopurinol.objects.filter(user=self.request.user),
            'febuxostat_list': Febuxostat.objects.filter(user=self.request.user),
            'colchicine_list': Colchicine.objects.filter(user=self.request.user),
            'ibuprofen_list': Ibuprofen.objects.filter(user=self.request.user),
            'celecoxib_list': Celecoxib.objects.filter(user=self.request.user),
            'meloxicam_list': Meloxicam.objects.filter(user=self.request.user),
            'naproxen_list': Naproxen.objects.filter(user=self.request.user),
            'prednisone_list': Prednisone.objects.filter(user=self.request.user),
            'probenecid_list': Probenecid.objects.filter(user=self.request.user),
            'methylprednisolone_list': Methylprednisolone.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class FlareView(ListView):
    template_name = 'treatment/flare.html'
    model = Colchicine

    def get_context_data(self, **kwargs):
        context = super(FlareView, self).get_context_data(**kwargs)
        context.update({
            'colchicine_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=False),
            'ibuprofen_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=False),
            'celecoxib_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=False),
            'meloxicam_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=False),
            'naproxen_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=False),
            'prednisone_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=False),
            'methylprednisolone_list': Methylprednisolone.objects.filter(user=self.request.user, as_injection=True),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class PreventionView(ListView):
    template_name = 'treatment/prevention.html'
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(PreventionView, self).get_context_data(**kwargs)
        context.update({
            'allopurinol_list': Allopurinol.objects.filter(user=self.request.user),
            'febuxostat_list': Febuxostat.objects.filter(user=self.request.user),
            'probenecid_list': Probenecid.objects.filter(user=self.request.user),
            'colchicine_ppx_list': Colchicine.objects.filter(user=self.request.user, as_prophylaxis=True),
            'ibuprofen_ppx_list': Ibuprofen.objects.filter(user=self.request.user, as_prophylaxis=True),
            'celecoxib_ppx_list': Celecoxib.objects.filter(user=self.request.user, as_prophylaxis=True),
            'meloxicam_ppx_list': Meloxicam.objects.filter(user=self.request.user, as_prophylaxis=True),
            'naproxen_ppx_list': Naproxen.objects.filter(user=self.request.user, as_prophylaxis=True),
            'prednisone_ppx_list': Prednisone.objects.filter(user=self.request.user, as_prophylaxis=True),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class AllopurinolDetail(DetailView):
    model = Allopurinol

class AllopurinolCreate(LoginRequiredMixin, CreateView):
    model = Allopurinol
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'de_sensitized',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        try:
            user_allopurinol = self.model.objects.get(user=self.request.user)
        except Allopurinol.DoesNotExist:
            user_allopurinol = None
        if user_allopurinol:
            return redirect("treatment:allopurinol-update", pk=self.model.objects.get(user=self.request.user).pk)
        else:
            return super(AllopurinolCreate, self).get(*args, **kwargs)

class AllopurinolUpdate(LoginRequiredMixin, UpdateView):
    model = Allopurinol
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'de_sensitized',]
    template_name = 'treatment/allopurinol_update.html'

class FebuxostatDetail(DetailView):
    model = Febuxostat

class FebuxostatCreate(LoginRequiredMixin, CreateView):
    model = Febuxostat
    fields = ['dose', 'date_started', 'date_ended', 'side_effects',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        try:
            user_febuxostat = self.model.objects.get(user=self.request.user)
        except Febuxostat.DoesNotExist:
            user_febuxostat = None
        if user_febuxostat:
            return redirect("treatment:febuxostat-update", pk=self.model.objects.get(user=self.request.user).pk)
        else:
            return super(FebuxostatCreate, self).get(*args, **kwargs)

class FebuxostatUpdate(LoginRequiredMixin, UpdateView):
    model = Febuxostat
    fields = ['dose', 'date_started', 'date_ended', 'side_effects',]
    template_name = 'treatment/febuxostat_update.html'

class ColchicineDetail(DetailView):
    model = Colchicine

class ColchicineCreate(LoginRequiredMixin, CreateView):
    model = Colchicine
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ColchicineUpdate(LoginRequiredMixin, UpdateView):
    model = Colchicine
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]
    template_name = 'treatment/colchicine_update.html'

class IbuprofenDetail(DetailView):
    model = Ibuprofen

class IbuprofenCreate(LoginRequiredMixin, CreateView):
    model = Ibuprofen
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class IbuprofenUpdate(LoginRequiredMixin, UpdateView):
    model = Ibuprofen
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis' ]
    template_name = 'treatment/ibuprofen_update.html'

class NaproxenDetail(DetailView):
    model = Naproxen

class NaproxenCreate(LoginRequiredMixin, CreateView):
    model = Naproxen
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NaproxenUpdate(LoginRequiredMixin, UpdateView):
    model = Naproxen
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]
    template_name = 'treatment/naproxen_update.html'

class MeloxicamDetail(DetailView):
    model = Meloxicam

class MeloxicamCreate(LoginRequiredMixin, CreateView):
    model = Meloxicam
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MeloxicamUpdate(LoginRequiredMixin, UpdateView):
    model = Meloxicam
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]
    template_name = 'treatment/meloxicam_update.html'

class CelecoxibDetail(DetailView):
    model = Celecoxib

class CelecoxibCreate(LoginRequiredMixin, CreateView):
    model = Celecoxib
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CelecoxibUpdate(LoginRequiredMixin, UpdateView):
    model = Celecoxib
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]
    template_name = 'treatment/celecoxib_update.html'

class PrednisoneDetail(DetailView):
    model = Prednisone

class PrednisoneCreate(LoginRequiredMixin, CreateView):
    model = Prednisone
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PrednisoneUpdate(LoginRequiredMixin, UpdateView):
    model = Prednisone
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'as_prophylaxis',]
    template_name = 'treatment/prednisone_update.html'

class MethylprednisoloneDetail(DetailView):
    model = Methylprednisolone

class MethylprednisoloneCreate(LoginRequiredMixin, CreateView):
    model = Methylprednisolone
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', 'as_injection',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MethylprednisoloneUpdate(LoginRequiredMixin, UpdateView):
    model = Methylprednisolone
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'as_injection',]
    template_name = 'treatment/methylprednisolone_update.html'

class ProbenecidDetail(DetailView):
    model = Probenecid

class ProbenecidCreate(LoginRequiredMixin, CreateView):
    model = Probenecid
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        try:
            user_probenecid = self.model.objects.get(user=self.request.user)
        except Probenecid.DoesNotExist:
            user_probenecid = None
        if user_probenecid:
            return redirect("treatment:probenecid-update", pk=self.model.objects.get(user=self.request.user).pk)
        else:
            return super(ProbenecidCreate, self).get(*args, **kwargs)

class ProbenecidUpdate(LoginRequiredMixin, UpdateView):
    model = Probenecid
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', ]
    template_name = 'treatment/probenacid_update.html'
    success_url = reverse_lazy('treatment:dashboard')    

class TinctureoftimeDetail(DetailView):
    model = Tinctureoftime

class TinctureoftimeCreate(LoginRequiredMixin, CreateView):
    model = Tinctureoftime
    fields = ['duration', 'date_started', 'date_ended', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        try:
            user_tinctureoftime = self.model.objects.get(user=self.request.user)
        except Tinctureoftime.DoesNotExist:
            user_tinctureoftime = None
        if user_tinctureoftime:
            return redirect("treatment:tinctureoftime-update", pk=self.model.objects.get(user=self.request.user).pk)
        else:
            return super(TinctureoftimeCreate, self).get(*args, **kwargs)

class TinctureoftimeUpdate(LoginRequiredMixin, UpdateView):
    model = Tinctureoftime
    fields = ['duration', 'date_started', 'date_ended', ]
    template_name = 'treatment/tinctureoftime_update.html'
    success_url = reverse_lazy('treatment:dashboard')    

class OthertreatDetail(DetailView):
    model = Othertreat

class OthertreatCreate(LoginRequiredMixin, CreateView):
    model = Othertreat
    fields = ['name', 'description', 'created', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        try:
            user_other = self.model.objects.get(user=self.request.user)
        except Othertreat.DoesNotExist:
            user_other = None
        if user_other:
            return redirect("treatment:othertreat-update", pk=self.model.objects.get(user=self.request.user).pk)
        else:
            return super(OthertreatCreate, self).get(*args, **kwargs)

class OthertreatUpdate(LoginRequiredMixin, UpdateView):
    model = Othertreat
    fields = ['name', 'description', 'created', ]
    template_name = 'treatment/othertreat_update.html'
    success_url = reverse_lazy('treatment:dashboard')    