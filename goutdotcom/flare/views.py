from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from ..history.forms import (
    AnginaForm,
    CHFSimpleForm,
    HeartAttackSimpleForm,
    HypertensionSimpleForm,
    PVDForm,
    StrokeSimpleForm,
)
from ..history.models import CHF, PVD, Angina, HeartAttack, Hypertension, Stroke
from ..lab.forms import UrateFlareForm
from ..lab.models import Urate
from .forms import FlareForm
from .models import Flare

# Create your views here.


class AboutFlares(TemplateView):
    template_name = "flare/about.html"


class FlareDetail(DetailView):
    model = Flare
    ### NEED TO CHECK IF FLARE BELONGS TO LOGGED IN USER, PERMISSION DENIED IF NOT


class FlareList(LoginRequiredMixin, ListView):
    """Changed allow_empty to = False so it returns 404 when empty, then redirect with dispatch to Flare About view"""

    allow_empty = False
    paginate_by = 5
    model = Flare
    """Overrode dispatch to redirect to Flare About view if FlareList view returns 404, as in the case of it being empty due to allow_empty=False
    """

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Http404:
            messages.info(self.request, f"No flares to list!")
            return redirect("flare:about")

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update(
            {
                "flare_list": Flare.objects.filter(user=self.request.user),
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by("-created")


class FlareCreate(CreateView):
    model = Flare
    form_class = FlareForm
    urate_form_class = UrateFlareForm
    angina_form_class = AnginaForm
    hypertension_form_class = HypertensionSimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    CHF_form_class = CHFSimpleForm
    stroke_form_class = StrokeSimpleForm
    PVD_form_class = PVDForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if self.request.user.patientprofile:
                if self.request.user.patientprofile.gender:
                    if self.request.user.patientprofile.gender == "male":
                        form.instance.male = True
                    else:
                        form.instance.male = False
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FlareCreate, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if "urate_form" not in context:
                context["urate_form"] = self.urate_form_class(self.request.GET)
            if "angina_form" not in context:
                context["angina_form"] = self.angina_form_class(instance=self.request.user.medicalprofile.angina)
            if "hypertension_form" not in context:
                context["hypertension_form"] = self.hypertension_form_class(
                    instance=self.request.user.medicalprofile.hypertension
                )
            if "heartattack_Form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    instance=self.request.user.medicalprofile.heartattack
                )
            if "CHF_form" not in context:
                context["CHF_form"] = self.CHF_form_class(instance=self.request.user.medicalprofile.CHF)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.request.user.medicalprofile.stroke)
            if "PVD_form" not in context:
                context["PVD_form"] = self.PVD_form_class(instance=self.request.user.medicalprofile.PVD)
        else:
            if "urate_form" not in context:
                context["urate_form"] = self.urate_form_class(self.request.GET)
            if "angina_form" not in context:
                context["angina_form"] = self.angina_form_class(self.request.GET)
            if "hypertension_form" not in context:
                context["hypertension_form"] = self.hypertension_form_class(self.request.GET)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(self.request.GET)
            if "CHF_form" not in context:
                context["CHF_form"] = self.CHF_form_class(self.request.GET)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(self.request.GET)
            if "PVD_form" not in context:
                context["PVD_form"] = self.PVD_form_class(self.request.GET)
        return context

    def get_form_kwargs(self):
        """Ovewrites get_form_kwargs() to look for 'flare' kwarg in GET request, uses 'flare' to query database for associated flare for use in FlareAidForm
        returns: [dict: dict containing 'flare' kwarg for form]"""
        # Assign self.gender to None so FlareForm won't error on loading from GET request kwargs before calling super() which will overwrite kwargs
        self.gender = None
        # Checks if user is logged in, if they have a patient profile gender, and if so, assign to self.gender
        if self.request.user.is_authenticated:
            if self.request.user.patientprofile.gender:
                self.gender = self.request.user.patientprofile.gender
        kwargs = super(FlareCreate, self).get_form_kwargs()
        # Pass self.gender to FlareForm as kwarg for use in form processing of male field
        if self.gender:
            kwargs["gender"] = self.gender
        return kwargs

    def get_object(self):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=Flare())
        urate_form = self.urate_form_class(request.POST, instance=Urate())
        if request.user.is_authenticated:
            angina_form = self.angina_form_class(request.POST, instance=request.user.medicalprofile.angina)
            hypertension_form = self.hypertension_form_class(
                request.POST, instance=request.user.medicalprofile.hypertension
            )
            heartattack_form = self.heartattack_form_class(
                request.POST, instance=request.user.medicalprofile.heartattack
            )
            CHF_form = self.CHF_form_class(request.POST, instance=request.user.medicalprofile.CHF)
            stroke_form = self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke)
            PVD_form = self.PVD_form_class(request.POST, instance=request.user.medicalprofile.PVD)
        else:
            angina_form = self.angina_form_class(request.POST, instance=Angina())
            hypertension_form = self.hypertension_form_class(request.POST, instance=Hypertension())
            heartattack_form = self.heartattack_form_class(request.POST, instance=HeartAttack())
            CHF_form = self.CHF_form_class(request.POST, instance=CHF())
            stroke_form = self.stroke_form_class(request.POST, instance=Stroke())
            PVD_form = self.PVD_form_class(request.POST, instance=PVD())
        if form.is_valid():
            flare_data = form.save(commit=False)
            if urate_form.is_valid():
                urate_data = urate_form.save(commit=False)
                if urate_data.value:
                    if request.user.is_authenticated:
                        urate_data.user = request.user
                    urate_data.save()
                    flare_data.urate = urate_data
            angina_data = angina_form.save(commit=False)
            angina_data.last_modified = "Flare"
            angina_data.save()
            hypertension_data = hypertension_form.save(commit=False)
            hypertension_data.last_modified = "Flare"
            hypertension_data.save()
            heartattack_data = heartattack_form.save(commit=False)
            heartattack_data.last_modified = "Flare"
            heartattack_data.save()
            CHF_data = CHF_form.save(commit=False)
            CHF_data.last_modified = "Flare"
            CHF_data.save()
            stroke_data = stroke_form.save(commit=False)
            stroke_data.last_modified = "Flare"
            stroke_data.save()
            PVD_data = PVD_form.save(commit=False)
            PVD_data.last_modified = "Flare"
            PVD_data.save()
            flare_data.angina = angina_data
            flare_data.hypertension = hypertension_data
            flare_data.heartattack = heartattack_data
            flare_data.CHF = CHF_data
            flare_data.stroke = stroke_data
            flare_data.PVD = PVD_data
            flare_data.save()
            return self.form_valid(form)
        else:
            if request.user.is_authenticated:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        urate_form=self.urate_form_class(request.POST, instance=Urate()),
                        angina_form=self.angina_form_class(request.POST, instance=request.user.medicalprofile.angina),
                        hypertension_form=self.hypertension_form_class(
                            request.POST, instance=request.user.medicalprofile.hypertension
                        ),
                        heartattack_form=self.heartattack_form_class(
                            request.POST, instance=request.user.medicalprofile.heartattack
                        ),
                        CHF_form=self.CHF_form_class(request.POST, instance=request.user.medicalprofile.CHF),
                        stroke_form=self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke),
                        PVD_form=self.PVD_form_class(request.POST, instance=request.user.medicalprofile.PVD),
                    )
                )
            else:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        urate_form=self.urate_form_class(request.POST, instance=Urate()),
                        angina_form=self.angina_form_class(request.POST, instance=Angina()),
                        hypertension_form=self.hypertension_form_class(request.POST, instance=Hypertension()),
                        heartattack_form=self.heartattack_form_class(request.POST, instance=HeartAttack()),
                        CHF_form=self.CHF_form_class(request.POST, instance=CHF()),
                        stroke_form=self.stroke_form_class(request.POST, instance=Stroke()),
                        PVD_form=self.PVD_form_class(request.POST, instance=PVD()),
                    )
                )


class FlareUpdate(LoginRequiredMixin, UpdateView):
    model = Flare

    form_class = FlareForm
    urate_form_class = UrateFlareForm
    angina_form_class = AnginaForm
    hypertension_form_class = HypertensionSimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    CHF_form_class = CHFSimpleForm
    stroke_form_class = StrokeSimpleForm
    PVD_form_class = PVDForm

    def get_context_data(self, **kwargs):
        context = super(FlareUpdate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if self.request.POST:
            if "urate_form" not in context:
                context["urate_form"] = self.urate_form_class(self.request.POST, instance=self.object.urate)
            if "angina_form" not in context:
                context["angina_form"] = self.angina_form_class(instance=self.request.user.medicalprofile.angina)
            if "hypertension_form" not in context:
                context["hypertension_form"] = self.hypertension_form_class(
                    instance=self.request.user.medicalprofile.hypertension
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    instance=self.request.user.medicalprofile.heartattack
                )
            if "CHF_form" not in context:
                context["CHF_form"] = self.CHF_form_class(instance=self.request.user.medicalprofile.CHF)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.request.user.medicalprofile.stroke)
            if "PVD_form" not in context:
                context["PVD_form"] = self.PVD_form_class(instance=self.request.user.medicalprofile.PVD)
        else:
            if "urate_form" not in context:
                context["urate_form"] = self.urate_form_class(instance=self.object.urate)
            if "angina_form" not in context:
                context["angina_form"] = self.angina_form_class(instance=self.request.user.medicalprofile.angina)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    instance=self.request.user.medicalprofile.heartattack
                )
            if "hypertension_form" not in context:
                context["hypertension_form"] = self.angina_form_class(
                    instance=self.request.user.medicalprofile.hypertension
                )
            if "CHF_form" not in context:
                context["CHF_form"] = self.CHF_form_class(instance=self.request.user.medicalprofile.CHF)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.request.user.medicalprofile.stroke)
            if "PVD_form" not in context:
                context["PVD_form"] = self.PVD_form_class(instance=self.request.user.medicalprofile.PVD)
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            flare_data = form.save(commit=False)
            flare_data.user = request.user
            urate_form = self.urate_form_class(request.POST, instance=self.object.urate)
            angina_form = self.angina_form_class(request.POST, instance=request.user.medicalprofile.angina)
            hypertension_form = self.hypertension_form_class(
                request.POST, instance=request.user.medicalprofile.hypertension
            )
            heartattack_form = self.hypertension_form_class(
                request.POST, instance=request.user.medicalprofile.heartattack
            )
            CHF_form = self.CHF_form_class(request.POST, instance=request.user.medicalprofile.CHF)
            stroke_form = self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke)
            PVD_form = self.PVD_form_class(request.POST, instance=request.user.medicalprofile.PVD)
            if urate_form.is_valid():
                urate_data = urate_form.save(commit=False)
                if urate_data.value:
                    urate_data.user = request.user
                    urate_data.save()
                    flare_data.urate = urate_data
            angina_data = angina_form.save(commit=False)
            angina_data.last_modified = "Flare"
            angina_data.save()
            hypertension_data = hypertension_form.save(commit=False)
            hypertension_data.last_modified = "Flare"
            hypertension_data.save()
            heartattack_data = heartattack_form.save(commit=False)
            heartattack_data.last_modified = "Flare"
            heartattack_data.save()
            CHF_data = CHF_form.save(commit=False)
            CHF_data.last_modified = "Flare"
            CHF_data.save()
            stroke_data = stroke_form.save(commit=False)
            stroke_data.last_modified = "Flare"
            stroke_data.save()
            PVD_data = PVD_form.save(commit=False)
            PVD_data.last_modified = "Flare"
            PVD_data.save()
            flare_data.hypertension = hypertension_data
            flare_data.heartattack = heartattack_data
            flare_data.CHF = CHF_data
            flare_data.stroke = stroke_data
            flare_data.PVD = PVD_data
            flare_data.save()
            return HttpResponseRedirect(reverse("flare:detail", kwargs={"pk": flare_data.pk}))
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    urate_form=self.urate_form_class(request.POST, instance=Urate()),
                    angina_form=self.angina_form_class(request.POST, instance=request.user.medicalprofile.angina),
                    hypertension_form=self.hypertension_form_class(
                        request.POST, instance=request.user.medicalprofile.hypertension
                    ),
                    heartattack_form=self.heartattack_form_class(
                        request.POST, instance=request.user.medicalprofile.heartattack
                    ),
                    CHF_form=self.CHF_form_class(request.POST, instance=request.user.medicalprofile.CHF),
                    stroke_form=self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke),
                    PVD_form=self.PVD_form_class(request.POST, instance=request.user.medicalprofile.PVD),
                )
            )
