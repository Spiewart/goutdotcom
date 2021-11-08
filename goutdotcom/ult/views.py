from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import ULTForm
from .models import ULT
from ..history.forms import CKDSimpleForm, ErosionsForm, TophiForm, UrateKidneyStonesForm
from ..history.models import CKD, Erosions, Tophi, UrateKidneyStones


class ULTCreate(CreateView):
    model = ULT
    form_class = ULTForm
    CKD_form_class = CKDSimpleForm
    erosions_form_class = ErosionsForm
    tophi_form_class = TophiForm
    urate_kidney_stones_class = UrateKidneyStonesForm

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

    def post(self, request):
        form = self.form_class(request.POST, instance=ULT(), user=self.request.user)

        if form.is_valid():
            ult_data = form.save(commit=False)
            CKD_form = self.CKD_form_class(request.POST, instance=CKD())
            erosions_form = self.erosions_form_class(request.POST, instance=Erosions())
            tophi_form = self.tophi_form_class(request.POST, instance=Tophi())
            urate_kidney_stones_form = self.urate_kidney_stones_class(request.POST, instance=UrateKidneyStones())

            # Check if User is logged in and pull MedicalProfile OnetoOne fields and set them to the form instance
            if self.request.user.is_authenticated:
                ult_data.user = request.user
                CKD_form = self.CKD_form_class(request.POST, instance=self.request.user.medicalprofile.CKD)
                erosions_form = self.erosions_form_class(request.POST, instance=self.request.user.medicalprofile.erosions)
                tophi_form = self.tophi_form_class(request.POST, instance=self.request.user.medicalprofile.tophi)
                urate_kidney_stones_form = self.urate_kidney_stones_class(request.POST, instance=self.request.user.medicalprofile.urate_kidney_stones)
            CKD_data = CKD_form.save(commit=False)
            CKD_data.last_modified = "ULT"
            CKD_data.save()
            erosions_data = erosions_form.save(commit=False)
            erosions_data.last_modified = "ULT"
            erosions_data.save()
            tophi_data = tophi_form.save(commit=False)
            tophi_data.last_modified = "ULT"
            tophi_data.save()
            urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
            urate_kidney_stones_data.last_modified = "ULT"
            urate_kidney_stones_data.save()
            ult_data.ckd = CKD_data
            ult_data.erosions = erosions_data
            ult_data.tophi = tophi_data
            ult_data.urate_kidney_stones = urate_kidney_stones_data
            ult_data.save()
            return HttpResponseRedirect(reverse("ult:detail", kwargs={"pk": ult_data.pk}))
        else:
            if request.user.is_authenticated:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        CKD_form = self.CKD_form_class(request.POST, instance=self.request.user.medicalprofile.CKD),
                        erosions_form = self.erosions_form_class(request.POST, instance=self.request.user.medicalprofile.erosions),
                        tophi_form = self.tophi_form_class(request.POST, instance=self.request.user.medicalprofile.tophi),
                        urate_kidney_stones_form = self.urate_kidney_stones_class(request.POST, instance=self.request.user.medicalprofile.urate_kidney_stones),
                    )
                )
            else:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        CKD_form = self.CKD_form_class(request.POST, instance=CKD()),
                        erosions_form = self.erosions_form_class(request.POST, instance=Erosions()),
                        tophi_form = self.tophi_form_class(request.POST, instance=Tophi()),
                        urate_kidney_stones_form = self.urate_kidney_stones_class(request.POST, instance=UrateKidneyStones()),
                    )
                )


class ULTDetail(DetailView):
    model = ULT


class ULTUpdate(LoginRequiredMixin, UpdateView):
    model = ULT
    form_class = ULTForm

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object(), user=self.request.user)

        if form.is_valid():
            ult_data = form.save(commit=False)
            if self.request.user.is_authenticated:
                ult_data.user = request.user
                # links ULT view ckd field to medicalprofile.CKD field
                if self.request.user.medicalprofile.CKD.value == True:
                    ult_data.ckd = True
                elif self.request.user.medicalprofile.CKD.value == False:
                    ult_data.ckd = False
                elif self.request.user.medicalprofile.CKD.value == None:
                    if ult_data.ckd == True:
                        self.request.user.medicalprofile.CKD.value = True
                        self.request.user.medicalprofile.CKD.last_modified = "ULT"
                        self.request.user.medicalprofile.CKD.save()
                    elif ult_data.ckd == False:
                        self.request.user.medicalprofile.CKD.value = True
                        self.request.user.medicalprofile.CKD.last_modified = "ULT"
                        self.request.user.medicalprofile.CKD.save()
                    else:
                        self.request.user.medicalprofile.CKD.value = None
                        self.request.user.medicalprofile.CKD.last_modified = "ULT"
                        self.request.user.medicalprofile.CKD.save()
                # links ULT view stones field to medicalprofile.urate_kidney_stones field
                if self.request.user.medicalprofile.urate_kidney_stones.value == True:
                    ult_data.stones = True
                elif self.request.user.medicalprofile.urate_kidney_stones.value == False:
                    ult_data.stones = False
                elif self.request.user.medicalprofile.urate_kidney_stones.value == None:
                    if ult_data.stones == True:
                        self.request.user.medicalprofile.urate_kidney_stones.value = True
                        self.request.user.medicalprofile.urate_kidney_stones.save()
                    elif ult_data.stones == False:
                        self.request.user.medicalprofile.urate_kidney_stones.value = True
                        self.request.user.medicalprofile.urate_kidney_stones.save()
                    else:
                        self.request.user.medicalprofile.urate_kidney_stones.value = None
                        self.request.user.medicalprofile.urate_kidney_stones.save()
                # links ULT view erosions field to medicalprofile.erosions field
                if self.request.user.medicalprofile.erosions.value == True:
                    ult_data.erosions = True
                elif self.request.user.medicalprofile.erosions.value == False:
                    ult_data.erosions = False
                elif self.request.user.medicalprofile.erosions.value == None:
                    if ult_data.erosions == True:
                        self.request.user.medicalprofile.erosions.value = True
                        self.request.user.medicalprofile.erosions.save()
                    elif ult_data.erosions == False:
                        self.request.user.medicalprofile.erosions.value = True
                        self.request.user.medicalprofile.erosions.save()
                    else:
                        self.request.user.medicalprofile.erosions.value = None
                        self.request.user.medicalprofile.erosions.save()
                # links ULT view tophi field to medicalprofile.tophi field
                if self.request.user.medicalprofile.tophi.value == True:
                    ult_data.tophi = True
                elif self.request.user.medicalprofile.tophi.value == False:
                    ult_data.tophi = False
                elif self.request.user.medicalprofile.tophi.value == None:
                    if ult_data.tophi == True:
                        self.request.user.medicalprofile.tophi.value = True
                        self.request.user.medicalprofile.tophi.save()
                    elif ult_data.tophi == False:
                        self.request.user.medicalprofile.tophi.value = True
                        self.request.user.medicalprofile.tophi.save()
                    else:
                        self.request.user.medicalprofile.tophi.value = None
                        self.request.user.medicalprofile.tophi.save()
                # links ULT view uric_acid field to medicalprofile.hyperuricemia field
                if self.request.user.medicalprofile.hyperuricemia.value == True:
                    ult_data.uric_acid = True
                elif self.request.user.medicalprofile.hyperuricemia.value == False:
                    ult_data.uric_acid = False
                elif self.request.user.medicalprofile.hyperuricemia.value == None:
                    if ult_data.uric_acid == True:
                        self.request.user.medicalprofile.hyperuricemia.value = True
                        self.request.user.medicalprofile.hyperuricemia.save()
                    elif ult_data.uric_acid == False:
                        self.request.user.medicalprofile.hyperuricemia.value = True
                        self.request.user.medicalprofile.hyperuricemia.save()
                    else:
                        self.request.user.medicalprofile.hyperuricemia.value = None
                        self.request.user.medicalprofile.hyperuricemia.save()
            ult_data.save()
            return HttpResponseRedirect(reverse("ult:detail", kwargs={"pk": ult_data.pk}))
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                )
            )
