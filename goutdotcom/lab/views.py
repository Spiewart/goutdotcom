from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .models import Urate

# Create your views here.
class UrateCreate(CreateView):
    model = Urate


class UrateDetail(DetailView):
    model = Urate


class UrateList(ListView):
    model = Urate


