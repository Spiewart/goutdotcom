from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Allopurinol, Colchicine, Febuxostat, Ibuprofen, Celecoxib, Meloxicam, Naproxen

def index(request):
    return render(request, 'treatment/index.html')

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
