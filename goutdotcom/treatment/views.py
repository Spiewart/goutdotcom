from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .models import Allopurinol, Febuxostat

class AllopurinolDetail(DetailView):
    model = Allopurinol

class FebuxostatDetail(DetailView):
    model = Febuxostat

def index(request):
    return render(request, 'treatment/index.html')

def flare(request):
    return render(request, 'treatment/flare.html')

def prevention(request):
    return render(request, 'prevention/flare.html')

