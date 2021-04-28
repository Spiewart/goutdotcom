from django.db.models.deletion import SET_NULL
from django.db.models.fields import NullBooleanField
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

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)

class ULTDetail(DetailView):
    model = ULT

def index(request):
    return render(request, 'ult/index.html')
