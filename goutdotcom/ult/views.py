from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from ..history.forms import (
    CKDForm,
    ErosionsForm,
    HyperuricemiaForm,
    TophiForm,
    UrateKidneyStonesForm,
)
from ..history.models import CKD, Erosions, Hyperuricemia, Tophi, UrateKidneyStones
from ..utils.mixins import (
    PatientProviderCreateMixin,
    PatientProviderMixin,
    ProfileMixin,
    UserMixin,
)
from .forms import ULTForm
from .models import ULT

User = get_user_model()


class ULTCreate(PatientProviderCreateMixin, ProfileMixin, SuccessMessageMixin, UserMixin, CreateView):
    """ULT CreateView.
    Intended to be responsive to whether or not the User is a Patient or Provider
    Redirects to UpdateView if ULT exists for the intended User

    Returns:
        [redirect]: [redirects to DetailView if successful otherwise UpdateView]
    """

    model = ULT
    form_class = ULTForm
    CKD_form_class = CKDForm
    erosions_form_class = ErosionsForm
    hyperuricemia_form_class = HyperuricemiaForm
    tophi_form_class = TophiForm
    urate_kidney_stones_form_class = UrateKidneyStonesForm

    def get_context_data(self, **kwargs):
        context = super(ULTCreate, self).get_context_data(**kwargs)

        def get_blank_forms():
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(self.request.GET)
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(self.request.GET)
            if "hyperuricemia_form" not in context:
                context["hyperuricemia_form"] = self.hyperuricemia_form_class(self.request.GET)
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(self.request.GET)
            if "urate_kidney_stones_form" not in context:
                context["urate_kidney_stones_form"] = self.urate_kidney_stones_form_class(self.request.GET)

        if self.request.user.is_authenticated:
            # Check if there is a User/MedicalProfile via User/ProfileMixin
            if self.medicalprofile:
                if "CKD_form" not in context:
                    context["CKD_form"] = self.CKD_form_class(instance=self.medicalprofile.CKD)
                if "erosions_form" not in context:
                    context["erosions_form"] = self.erosions_form_class(instance=self.medicalprofile.erosions)
                if "hyperuricemia_form" not in context:
                    context["hyperuricemia_form"] = self.hyperuricemia_form_class(
                        instance=self.medicalprofile.hyperuricemia
                    )
                if "tophi_form" not in context:
                    context["tophi_form"] = self.tophi_form_class(instance=self.medicalprofile.tophi)
                if "urate_kidney_stones_form" not in context:
                    context["urate_kidney_stones_form"] = self.urate_kidney_stones_form_class(
                        instance=self.medicalprofile.urate_kidney_stones
                    )
            else:
                get_blank_forms()
        else:
            get_blank_forms()
        return context

    def get_success_url(self):
        # Check if there is a username kwarg and redirect to DetailView using that
        if self.kwargs.get("username"):
            return reverse("ult:user-detail", kwargs={"slug": self.kwargs["username"]})
        # Otherwise return to DetailView based on PK
        else:
            return reverse(
                "ult:detail",
                kwargs={
                    "pk": self.object.pk,
                },
            )

    def form_valid(self, form):
        # Add message to confirm successful ULT creation
        messages.success(self.request, "ULT created!")
        if self.request.user.is_authenticated:
            if self.user:
                form.instance.user = self.user
            form.instance.creator = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # get() is overwritten to redirect the User to a ULT if it already exists for the intended User
        # Check if User is logged in
        if self.request.user.is_authenticated:
            # Check if User is a Patient
            user_ULT = None
            if self.user:
                try:
                    user_ULT = self.model.objects.get(user=self.user)
                except ObjectDoesNotExist:
                    user_ULT = None
            # If a ULT already exists for the intended User, redirect to UpdateView
            if user_ULT:
                return redirect("ult:user-update", slug=user_ULT.slug)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Post is overwritten for multiform view
        form = self.form_class(request.POST, instance=ULT())
        CKD_form = self.CKD_form_class(request.POST, instance=CKD())
        erosions_form = self.erosions_form_class(request.POST, instance=Erosions())
        hyperuricemia_form = self.hyperuricemia_form_class(request.POST, instance=Hyperuricemia())
        tophi_form = self.tophi_form_class(request.POST, instance=Tophi())
        urate_kidney_stones_form = self.urate_kidney_stones_form_class(request.POST, instance=UrateKidneyStones())

        if form.is_valid():
            ult_data = form.save(commit=False)
            # Check if User is logged in
            # User/ProfileMixins provide MedicalProfile fields for form
            if self.request.user.is_authenticated:
                if self.medicalprofile:
                    CKD_form = self.CKD_form_class(request.POST, instance=self.medicalprofile.CKD)
                    erosions_form = self.erosions_form_class(request.POST, instance=self.medicalprofile.erosions)
                    hyperuricemia_form = self.hyperuricemia_form_class(
                        request.POST, instance=self.medicalprofile.hyperuricemia
                    )
                    tophi_form = self.tophi_form_class(request.POST, instance=self.medicalprofile.tophi)
                    urate_kidney_stones_form = self.urate_kidney_stones_form_class(
                        request.POST, instance=self.medicalprofile.urate_kidney_stones
                    )
            # Process related models/forms and set last_modified to "ULT"
            if CKD_form.is_valid():
                CKD_data = CKD_form.save(commit=False)
                CKD_data.last_modified = "ULT"
                CKD_data.save()
            if erosions_form.is_valid():
                erosions_data = erosions_form.save(commit=False)
                erosions_data.last_modified = "ULT"
                erosions_data.save()
            if hyperuricemia_form.is_valid():
                hyperuricemia_data = hyperuricemia_form.save(commit=False)
                hyperuricemia_data.last_modified = "ULT"
                hyperuricemia_data.save()
            if tophi_form.is_valid():
                tophi_data = tophi_form.save(commit=False)
                tophi_data.last_modified = "ULT"
                tophi_data.save()
            if urate_kidney_stones_form.is_valid():
                urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
                urate_kidney_stones_data.last_modified = "ULT"
                urate_kidney_stones_data.save()
            ult_data.ckd = CKD_data
            ult_data.erosions = erosions_data
            ult_data.hyperuricemia = hyperuricemia_data
            ult_data.tophi = tophi_data
            ult_data.stones = urate_kidney_stones_data
            return self.form_valid(form)
        else:
            # If form is not valid, check if User is logged in
            if request.user.is_authenticated:
                if self.medicalprofile:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            CKD_form=self.CKD_form_class(request.POST, instance=self.medicalprofile.CKD),
                            erosions_form=self.erosions_form_class(request.POST, instance=self.medicalprofile.erosions),
                            hyperuricemia_form=self.hyperuricemia_form_class(
                                request.POST, instance=self.medicalprofile.hyperuricemia
                            ),
                            tophi_form=self.tophi_form_class(request.POST, instance=self.medicalprofile.tophi),
                            urate_kidney_stones_form=self.urate_kidney_stones_form_class(
                                request.POST, instance=self.medicalprofile.urate_kidney_stones
                            ),
                        )
                    )
                else:
                    # Otherwise rerender form with new related model instances
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            CKD_form=self.CKD_form_class(request.POST, instance=CKD()),
                            erosions_form=self.erosions_form_class(request.POST, instance=Erosions()),
                            hyperuricemia_form=self.hyperuricemia_form_class(request.POST, instance=Hyperuricemia()),
                            tophi_form=self.tophi_form_class(request.POST, instance=Tophi()),
                            urate_kidney_stones_form=self.urate_kidney_stones_form_class(
                                request.POST, instance=UrateKidneyStones()
                            ),
                        )
                    )
            else:
                # Otherwise rerender form with new related model instances
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        CKD_form=self.CKD_form_class(request.POST, instance=CKD()),
                        erosions_form=self.erosions_form_class(request.POST, instance=Erosions()),
                        hyperuricemia_form=self.hyperuricemia_form_class(request.POST, instance=Hyperuricemia()),
                        tophi_form=self.tophi_form_class(request.POST, instance=Tophi()),
                        urate_kidney_stones_form=self.urate_kidney_stones_form_class(
                            request.POST, instance=UrateKidneyStones()
                        ),
                    )
                )


class ULTDetail(PatientProviderMixin, DetailView):
    model = ULT


class ULTUpdate(LoginRequiredMixin, PatientProviderMixin, ProfileMixin, UserMixin, UpdateView):
    """ULT UpdateView.
    Intended to be responsive to whether or not the User is a Patient or Provider

    Returns:
        [redirect]: [redirects to DetailView if successful]
    """

    model = ULT
    form_class = ULTForm
    CKD_form_class = CKDForm
    erosions_form_class = ErosionsForm
    hyperuricemia_form_class = HyperuricemiaForm
    tophi_form_class = TophiForm
    urate_kidney_stones_form_class = UrateKidneyStonesForm

    def get_context_data(self, **kwargs):
        context = super(ULTUpdate, self).get_context_data(**kwargs)
        # Add FlareAid OnetoOne related model objects from the MedicalProfile for fetched User
        if self.request.POST:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(
                    self.request.POST, instance=self.object.CKD, prefix="CKD_form"
                )
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(
                    self.request.POST, instance=self.object.erosions, prefix="erosions_form"
                )
            if "hyperuricemia_form" not in context:
                context["hyperuricemia_form"] = self.hyperuricemia_form_class(
                    self.request.POST, instance=self.object.hyperuricemia, prefix="hyperuricemia_form"
                )
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(
                    self.request.POST, instance=self.object.tophi, prefix="tophi_form"
                )
            if "urate_kidney_stones_form" not in context:
                context["urate_kidney_stones_form"] = self.urate_kidney_stones_form_class(
                    self.request.POST,
                    instance=self.object.stones,
                    prefix="urate_kidney_stones_form",
                )
        else:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.object.ckd, prefix="CKD_form")
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(
                    instance=self.object.erosions, prefix="erosions_form"
                )
            if "hyperuricemia_form" not in context:
                context["hyperuricemia_form"] = self.hyperuricemia_form_class(
                    instance=self.object.hyperuricemia, prefix="hyperuricemia_form"
                )
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(instance=self.object.tophi, prefix="tophi_form")
            if "urate_kidney_stones_form" not in context:
                context["urate_kidney_stones_form"] = self.urate_kidney_stones_form_class(
                    instance=self.object.stones, prefix="urate_kidney_stones_form"
                )
        return context

    def get_success_url(self):
        # Check if there is a slug kwarg and redirect to DetailView using that
        if self.kwargs.get("slug"):
            return reverse("ult:user-detail", kwargs={"slug": self.kwargs["slug"]})
        # Otherwise return to DetailView based on PK
        else:
            return reverse(
                "ult:detail",
                kwargs={
                    "pk": self.object.pk,
                },
            )

    def form_valid(self, form):
        # Success message
        messages.success(self.request, "ULT updated!")
        return super().form_valid(form)

    def post(self, request, **kwargs):
        self.object = self.get_object()
        # Post overwritten to process multiple forms
        form = self.form_class(request.POST, instance=self.object)
        # Fetch related models from existing ULT object
        CKD_form = self.CKD_form_class(request.POST, instance=self.object.ckd, prefix="CKD_form")
        erosions_form = self.erosions_form_class(request.POST, instance=self.object.erosions, prefix="erosions_form")
        hyperuricemia_form = self.hyperuricemia_form_class(
            request.POST, instance=self.object.hyperuricemia, prefix="hyperuricemia_form"
        )
        tophi_form = self.tophi_form_class(request.POST, instance=self.object.tophi, prefix="tophi_form")
        urate_kidney_stones_form = self.urate_kidney_stones_form_class(
            request.POST, instance=self.object.stones, prefix="urate_kidney_stones_form"
        )
        if form.is_valid():
            # Check if form and related model forms are valid to process
            ult_data = form.save(commit=False)
            if CKD_form.is_valid():
                CKD_data = CKD_form.save(commit=False)
                CKD_data.last_modified = "ULT"
                CKD_data.save()
            if erosions_form.is_valid():
                erosions_data = erosions_form.save(commit=False)
                erosions_data.last_modified = "ULT"
                erosions_data.save()
            if hyperuricemia_form.is_valid():
                hyperuricemia_data = hyperuricemia_form.save(commit=False)
                hyperuricemia_data.last_modified = "ULT"
                hyperuricemia_data.save()
            if tophi_form.is_valid():
                tophi_data = tophi_form.save(commit=False)
                tophi_data.last_modified = "ULT"
                tophi_data.save()
            if urate_kidney_stones_form.is_valid():
                urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
                urate_kidney_stones_data.last_modified = "ULT"
                urate_kidney_stones_data.save()
            ult_data.ckd = CKD_data
            ult_data.erosions = erosions_data
            ult_data.hyperuricemia = hyperuricemia_data
            ult_data.tophi = tophi_data
            ult_data.stones = urate_kidney_stones_data
            return self.form_valid(form)

        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    CKD_form=self.CKD_form_class(request.POST, instance=self.object.CKD),
                    erosions_form=self.erosions_form_class(request.POST, instance=self.object.erosions),
                    hyperuricemia_form=self.hyperuricemia_form_class(request.POST, instance=self.object.hyperuricemia),
                    tophi_form=self.tophi_form_class(request.POST, instance=self.object.tophi),
                    urate_kidney_stones_form=self.urate_kidney_stones_form_class(
                        request.POST, instance=self.object.stones
                    ),
                )
            )
