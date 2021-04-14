from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField

from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .forms import ULTForm
from .models import ULT

# Create your views here.

class ULTCreate(CreateView):
    model = ULT
    form_class = ULTForm

class ULTDetail(DetailView):
    model = ULT


def index(request):
    return render(request, 'ult/index.html')
