from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .models import ULT

# Create your views here.


class ULTCreate(CreateView):
    fields = '__all__'
    model = ULT


class ULTDetail(DetailView):
    model = ULT


def index(request):
    return render(request, 'ult/index.html')
