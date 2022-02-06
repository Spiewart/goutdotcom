from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
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
from ..utils.mixins import PatientProviderMixin
from .forms import ULTForm
from .models import ULT

User = get_user_model()


class ULTCreate(SuccessMessageMixin, CreateView):
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
        if self.request.user.is_authenticated:
            # If User is logged in, see if there is username kwarg
            try:
                self.username = self.kwargs.get("username")
            except:
                self.username = None
            # If there is a username, fetch associated User and related MedicalProfile objects
            # Add forms with User's related model instances
            if self.username:
                # Fetch related model instances via User object
                self.user = User.objects.get(username=self.username)
                if "CKD_form" not in context:
                    context["CKD_form"] = self.CKD_form_class(instance=self.user.medicalprofile.CKD)
                if "erosions_form" not in context:
                    context["erosions_form"] = self.erosions_form_class(instance=self.user.medicalprofile.erosions)
                if "hyperuricemia_form" not in context:
                    context["hyperuricemia_form"] = self.hyperuricemia_form_class(
                        instance=self.user.medicalprofile.hyperuricemia
                    )
                if "tophi_form" not in context:
                    context["tophi_form"] = self.tophi_form_class(instance=self.user.medicalprofile.tophi)
                if "urate_kidney_stones_form" not in context:
                    context["urate_kidney_stones_form"] = self.urate_kidney_stones_form_class(
                        instance=self.user.medicalprofile.urate_kidney_stones
                    )
                return context
            # Else render forms as new model instances
            else:
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
                return context
        else:
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
            return context

    def get_success_url(self):
        # Check if there is a username kwarg and redirect to DetailView using that
        if self.kwargs.get("username"):
            return reverse("ult:user-detail", kwargs={"slug": self.kwargs["username"]})
        # Otherwise return to DetailView based on PK
        else:
            return reverse(
                "ult:detail",
                # Need comma at end of kwargs for some picky Django reason
                # https://stackoverflow.com/questions/52575418/reverse-with-prefix-argument-after-must-be-an-iterable-not-int/52575419
                kwargs={
                    "pk": self.object.pk,
                },
            )

    def form_valid(self, form):
        # Add message to confirm successful ULT creation
        messages.success(self.request, "ULT created!")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # get() is overwritten to redirect the User to a ULT if it already exists for the intended User
        # Check if User is logged in
        if self.request.user.is_authenticated:
            # Check if User is a Patient
            if request.user.role == "PATIENT":
                # If so, try to fetch ULT and assign to user_ULT
                try:
                    user_ULT = self.model.objects.get(user=request.user)
                # Else set to None
                except:
                    user_ULT = None
            # Check if User is a Provider
            elif request.user.role == "PROVIDER":
                # Check if there is a username in kwargs
                try:
                    self.username = self.kwargs.get("username")
                # Assign to None otherwise
                except:
                    self.username = None
                # If there is a username in kwargs, fetch the User its associated with
                if self.username:
                    self.user = User.objects.get(username=self.username)
                    # Check if there is a ULT for that User
                    try:
                        user_ULT = self.model.objects.get(user=self.user)
                    # Assign to None otherwise
                    except self.model.DoesNotExist:
                        user_ULT = None
            # If a ULT already exists for the intended User, redirect to UpdateView
            if user_ULT:
                return redirect("ult:user-update", slug=user_ULT.slug)
            # Otherwise return super().get()
            else:
                return super().get(request, *args, **kwargs)
        # If User is not logged in, return super().get()
        else:
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
            # Check if User is logged in and pull MedicalProfile OnetoOne fields and set them to the form instance
            if self.request.user.is_authenticated:
                # If User is logged in, see if there is username kwarg
                try:
                    self.username = self.kwargs.get("username")
                except:
                    self.username = None
                # If there is a username, fetch associated User and related MedicalProfile objects
                # Overwrite forms defined above with User instances
                if self.username:
                    self.user = User.objects.get(username=self.username)
                    # Assign User to ULT form to avoid repeating the query in form_valid()
                    ult_data.user = self.user
                    CKD_form = self.CKD_form_class(request.POST, instance=self.user.medicalprofile.CKD)
                    erosions_form = self.erosions_form_class(request.POST, instance=self.user.medicalprofile.erosions)
                    hyperuricemia_form = self.hyperuricemia_form_class(
                        request.POST, instance=self.user.medicalprofile.hyperuricemia
                    )
                    tophi_form = self.tophi_form_class(request.POST, instance=self.user.medicalprofile.tophi)
                    urate_kidney_stones_form = self.urate_kidney_stones_form_class(
                        request.POST, instance=self.user.medicalprofile.urate_kidney_stones
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
                # Check if username kwarg was supplied
                try:
                    self.username = self.kwargs.get("username")
                except:
                    self.username = None
                # If so, fetch related model instances and rerender form
                if self.username:
                    self.user = User.objects.get(username=self.username)
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            CKD_form=self.CKD_form_class(request.POST, instance=self.user.medicalprofile.CKD),
                            erosions_form=self.erosions_form_class(
                                request.POST, instance=self.user.medicalprofile.erosions
                            ),
                            hyperuricemia_form=self.hyperuricemia_form_class(
                                request.POST, instance=self.user.medicalprofile.hyperuricemia
                            ),
                            tophi_form=self.tophi_form_class(request.POST, instance=self.user.medicalprofile.tophi),
                            urate_kidney_stones_form=self.urate_kidney_stones_form_class(
                                request.POST, instance=self.user.medicalprofile.urate_kidney_stones
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


class ULTUpdate(LoginRequiredMixin, UpdateView):
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
        # Fetch username from slug kwarg
        self.username = self.kwargs.get("slug")
        # Fetch user from username
        self.user = User.objects.get(username=self.username)
        # Add FlareAid OnetoOne related model objects from the MedicalProfile for fetched User
        if self.request.POST:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(
                    self.request.POST, instance=self.user.medicalprofile.CKD, prefix="CKD_form"
                )
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(
                    self.request.POST, instance=self.user.medicalprofile.erosions, prefix="erosions_form"
                )
            if "hyperuricemia_form" not in context:
                context["hyperuricemia_form"] = self.hyperuricemia_form_class(
                    self.request.POST, instance=self.user.medicalprofile.hyperuricemia, prefix="hyperuricemia_form"
                )
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(
                    self.request.POST, instance=self.user.medicalprofile.tophi, prefix="tophi_form"
                )
            if "urate_kidney_stones_form" not in context:
                context["urate_kidney_stones_form"] = self.urate_kidney_stones_form_class(
                    self.request.POST,
                    instance=self.user.medicalprofile.urate_kidney_stones,
                    prefix="urate_kidney_stones_form",
                )
            return context
        else:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.user.medicalprofile.CKD, prefix="CKD_form")
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(
                    instance=self.user.medicalprofile.erosions, prefix="erosions_form"
                )
            if "hyperuricemia_form" not in context:
                context["hyperuricemia_form"] = self.hyperuricemia_form_class(
                    instance=self.user.medicalprofile.hyperuricemia, prefix="hyperuricemia_form"
                )
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(
                    instance=self.user.medicalprofile.tophi, prefix="tophi_form"
                )
            if "urate_kidney_stones_form" not in context:
                context["urate_kidney_stones_form"] = self.urate_kidney_stones_form_class(
                    instance=self.user.medicalprofile.urate_kidney_stones, prefix="urate_kidney_stones_form"
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
                # Need comma at end of kwargs for some picky Django reason
                # https://stackoverflow.com/questions/52575418/reverse-with-prefix-argument-after-must-be-an-iterable-not-int/52575419
                kwargs={
                    "pk": self.object.pk,
                },
            )

    def form_valid(self, form):
        # Success message
        messages.success(self.request, "ULT updated!")
        return super().form_valid(form)

    def post(self, request, **kwargs):
        # Post overwritten to process multiple forms
        form = self.form_class(request.POST, instance=self.get_object())
        # Fetch related models from existing ULT object
        CKD_form = self.CKD_form_class(request.POST, instance=form.instance.ckd, prefix="CKD_form")
        erosions_form = self.erosions_form_class(request.POST, instance=form.instance.erosions, prefix="erosions_form")
        hyperuricemia_form = self.hyperuricemia_form_class(
            request.POST, instance=form.instance.hyperuricemia, prefix="hyperuricemia_form"
        )
        tophi_form = self.tophi_form_class(request.POST, instance=form.instance.tophi, prefix="tophi_form")
        urate_kidney_stones_form = self.urate_kidney_stones_form_class(
            request.POST, instance=form.instance.stones, prefix="urate_kidney_stones_form"
        )
        if form.is_valid():
            # Check if form and related model forms are valid to process
            ult_data = form.save(commit=False)
            if CKD_form.is_valid():
                CKD_data = CKD_form.save(commit=False)
                CKD_data.last_modified = "ULT"
                CKD_data.pk = CKD_form.instance.pk
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
                    CKD_form=self.CKD_form_class(request.POST, instance=self.user.medicalprofile.CKD),
                    erosions_form=self.erosions_form_class(request.POST, instance=self.user.medicalprofile.erosions),
                    hyperuricemia_form=self.hyperuricemia_form_class(
                        request.POST, instance=self.user.medicalprofile.hyperuricemia
                    ),
                    tophi_form=self.tophi_form_class(request.POST, instance=self.user.medicalprofile.tophi),
                    urate_kidney_stones_form=self.urate_kidney_stones_form_class(
                        request.POST, instance=self.user.medicalprofile.urate_kidney_stones
                    ),
                )
            )
