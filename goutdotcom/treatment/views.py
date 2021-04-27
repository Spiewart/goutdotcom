from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Allopurinol, Colchicine, Febuxostat, Ibuprofen, Celecoxib, Meloxicam, Naproxen, Prednisone, Probenecid, Methylprednisolone

class IndexView(ListView):
    template_name = 'treatment/index.html'
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'allopurinol_list': Allopurinol.objects.filter(user=self.request.user),
            'febuxostat_list': Febuxostat.objects.filter(user=self.request.user), 
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

def flare(request):
    return render(request, 'treatment/flare.html')

def prevention(request):
    return render(request, 'prevention/flare.html')

class AllopurinolDetail(DetailView):
    model = Allopurinol

class AllopurinolCreate(LoginRequiredMixin, CreateView):
    model = Allopurinol
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'de_sensitized',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AllopurinolUpdate(LoginRequiredMixin, UpdateView):
    model = Allopurinol
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', 'de_sensitized',]

class FebuxostatDetail(DetailView):
    model = Febuxostat

class FebuxostatCreate(LoginRequiredMixin, CreateView):
    model = Febuxostat
    fields = ['dose', 'date_started', 'date_ended', 'side_effects',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FebuxostatUpdate(LoginRequiredMixin, UpdateView):
    model = Febuxostat
    fields = ['dose', 'date_started', 'date_ended', 'side_effects',]

class ColchicineDetail(DetailView):
    model = Colchicine

class ColchicineCreate(LoginRequiredMixin, CreateView):
    model = Colchicine
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ColchicineUpdate(LoginRequiredMixin, UpdateView):
    model = Colchicine
    fields = ['dose', 'date_started', 'date_ended', 'side_effects',]

class IbuprofenDetail(DetailView):
    model = Ibuprofen

class IbuprofenCreate(LoginRequiredMixin, CreateView):
    model = Ibuprofen
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class IbuprofenUpdate(LoginRequiredMixin, UpdateView):
    model = Ibuprofen
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', ]

class NaproxenDetail(DetailView):
    model = Naproxen

class NaproxenCreate(LoginRequiredMixin, CreateView):
    model = Naproxen
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NaproxenUpdate(LoginRequiredMixin, UpdateView):
    model = Naproxen
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', ]

class MeloxicamDetail(DetailView):
    model = Meloxicam

class MeloxicamCreate(LoginRequiredMixin, CreateView):
    model = Meloxicam
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MeloxicamUpdate(LoginRequiredMixin, UpdateView):
    model = Meloxicam
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', ]

class CelecoxibDetail(DetailView):
    model = Celecoxib

class CelecoxibCreate(LoginRequiredMixin, CreateView):
    model = Celecoxib
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CelecoxibUpdate(LoginRequiredMixin, UpdateView):
    model = Celecoxib
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', ]

class PrednisoneDetail(DetailView):
    model = Prednisone

class PrednisoneCreate(LoginRequiredMixin, CreateView):
    model = Prednisone
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PrednisoneUpdate(LoginRequiredMixin, UpdateView):
    model = Prednisone
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', ]

class MethylprednisoloneDetail(DetailView):
    model = Methylprednisolone

class MethylprednisoloneCreate(LoginRequiredMixin, CreateView):
    model = Methylprednisolone
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MethylprednisoloneUpdate(LoginRequiredMixin, UpdateView):
    model = Methylprednisolone
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', ]

class ProbenecidDetail(DetailView):
    model = Probenecid

class ProbenecidCreate(LoginRequiredMixin, CreateView):
    model = Probenecid
    fields = ['dose', 'freq', 'date_started', 'date_ended', 'side_effects', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProbenecidUpdate(LoginRequiredMixin, UpdateView):
    model = Probenecid
    fields = ['dose', 'date_started', 'date_ended', 'side_effects', ]