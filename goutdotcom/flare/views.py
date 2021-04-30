from goutdotcom.flare.forms import FlareForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Flare
from .forms import FlareForm
# Create your views here.
def index(request):
    return render(request, 'flare/index.html')

class FlareCreate(LoginRequiredMixin, CreateView):
    model = Flare
    form_class = FlareForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FlareDetail(LoginRequiredMixin, DetailView):
    model = Flare

class FlareUpdate(LoginRequiredMixin, UpdateView):
    model = Flare
    fields = ['location', 'treatment', 'colchicine', 'ibuprofen', 'naproxen', 'celecoxib', 'meloxicam', 'prednisone', 'methylprednisolone', 'duration', 'urate_draw', 'urate']
    template_name = 'flare/flare_update.html'