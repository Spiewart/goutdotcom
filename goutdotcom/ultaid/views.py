from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import ULTAidForm
from .models import ULTAid

# Create your views here.

class ULTAidCreate(CreateView):
    model = ULTAid
    form_class = ULTAidForm

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
                return redirect("ultaid:update", pk=self.model.objects.get(user=self.request.user).pk)
            else:
                return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

class ULTAidDetail(DetailView):
    model = ULTAid

class ULTAidUpdate(LoginRequiredMixin, UpdateView):
    model = ULTAid
    form_class=ULTAidForm
