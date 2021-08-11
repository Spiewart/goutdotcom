from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, UpdateView
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

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                user_ULT = self.model.objects.get(user=self.request.user)
            except self.model.DoesNotExist:
                user_ULT = None
            if user_ULT:
                return redirect("ult:update", pk=self.model.objects.get(user=self.request.user).pk)
            else:
                return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

class ULTDetail(DetailView):
    model = ULT

class ULTUpdate(LoginRequiredMixin, UpdateView):
    model = ULT
    form_class=ULTForm

def index(request):
    return render(request, 'ult/index.html')
