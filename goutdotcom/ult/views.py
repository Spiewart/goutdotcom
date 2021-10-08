from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from ..history.forms import CKDForm, ErosionsForm, TophiForm, UrateKidneyStonesForm
from ..history.models import CKD, Erosions, Tophi, UrateKidneyStones
from .forms import ULTForm
from .models import ULT

# Create your views here.


class ULTCreate(CreateView):
    model = ULT
    form_class = ULTForm
    CKD_form_class = CKDForm
    erosions_form_class = ErosionsForm
    tophi_form_class = TophiForm
    urate_kidney_stones_form_class = UrateKidneyStonesForm

    def get_context_data(self, **kwargs):
        context = super(ULTCreate, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context.update({"user": self.request.user})
        if "CKD_form" not in context:
            context["CKD_form"] = self.CKD_form_class(self.request.GET)
        if "erosions_form" not in context:
            context["erosions_form"] = self.erosions_form_class(self.request.GET)
        if "tophi_form" not in context:
            context["tophi_form"] = self.tophi_form_class(self.request.GET)
        if "urate_kidney_stones_form" not in context:
            context["urate_kidney_stones_form"] = self.urate_kidney_stones_form_class(self.request.GET)
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_object(self, queryset=None):
        object = self.model
        return object

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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=ULT())
        CKD_form = self.CKD_form_class(request.POST, instance=CKD())
        erosions_form = self.erosions_form_class(request.POST, instance=Erosions())
        tophi_form = self.tophi_form_class(request.POST, instance=Tophi())
        urate_kidney_stones_form = self.urate_kidney_stones_form_class(request.POST, instance=UrateKidneyStones())

        if (
            form.is_valid()
            and CKD_form.is_valid()
            and erosions_form.is_valid()
            and tophi_form.is_valid()
            and urate_kidney_stones_form.is_valid()
        ):
            ULT_data = form.save(commit=False)
            if request.user.is_authenticated:
                CKD_data = CKD_form.save(commit=False)
                CKD_data.pk = None
                erosions_data = erosions_form.save(commit=False)
                tophi_data = tophi_form.save(commit=False)
                urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
                ULT_data.user = request.user
                CKD_data.user = request.user
                CKD_data.save()
                erosions_data.user = request.user
                erosions_data.save()
                tophi_data.user = request.user
                tophi_data.save()
                urate_kidney_stones_data.user = request.user
                urate_kidney_stones_data.save()
                ULT_data.CKD = CKD_data
                ULT_data.erosions = erosions_data
                ULT_data.tophi = tophi_data
                ULT_data.urate_kidney_stones = urate_kidney_stones_data
            else:
                CKD_data = CKD_form.save(commit=False)
                erosions_data = erosions_form.save(commit=False)
                tophi_data = tophi_form.save(commit=False)
                urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
                CKD_data.pk = None
                CKD_data.save()
                erosions_data.save()
                tophi_data.save()
                urate_kidney_stones_data.save()
                ULT_data.CKD = CKD_data
                ULT_data.erosions = erosions_data
                ULT_data.tophi = tophi_data
                ULT_data.urate_kidney_stones = urate_kidney_stones_data
            ULT_data.save()
            return HttpResponseRedirect(reverse("ult:detail", kwargs={"pk": ULT_data.pk}))
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    CKD_form=CKD_form,
                    erosions_form=erosions_form,
                    tophi_form=tophi_form,
                    urate_kidney_stones_form=urate_kidney_stones_form,
                )
            )


class ULTDetail(DetailView):
    model = ULT


class ULTUpdate(LoginRequiredMixin, UpdateView):
    model = ULT
    form_class = ULTForm
