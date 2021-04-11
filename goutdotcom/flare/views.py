from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .models import ULT

# Create your views here.


class ULTCreate(CreateView):
    model = ULT

class ULTdetail(DetailView):
    model = ULT
