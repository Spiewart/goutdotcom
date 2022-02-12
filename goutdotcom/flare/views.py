from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
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
from ..utils.mixins import (
    PatientProviderCreateMixin,
    PatientProviderMixin,
    ProfileMixin,
    UserMixin,
)
from .forms import FlareForm
from .models import Flare

User = get_user_model()


class AboutFlares(TemplateView):
    template_name = "flare/about.html"


class FlareDetail(PatientProviderMixin, DetailView):
    model = Flare


class FlareList(LoginRequiredMixin, UserMixin, ListView):
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
                "flare_list": Flare.objects.filter(user=self.user),
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.user)


class FlareCreate(PatientProviderCreateMixin, ProfileMixin, UserMixin, CreateView):
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
            if self.patientprofile:
                if self.patientprofile.gender:
                    if self.user.patientprofile.gender == "male":
                        form.instance.male = True
                    else:
                        form.instance.male = False
                form.instance.user = self.user
            form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FlareCreate, self).get_context_data(**kwargs)

        def get_blank_forms():
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

        if self.request.user.is_authenticated:
            if self.user:
                if self.medicalprofile:
                    if "urate_form" not in context:
                        context["urate_form"] = self.urate_form_class(self.request.GET)
                    if "angina_form" not in context:
                        context["angina_form"] = self.angina_form_class(instance=self.medicalprofile.angina)
                    if "hypertension_form" not in context:
                        context["hypertension_form"] = self.hypertension_form_class(
                            instance=self.medicalprofile.hypertension
                        )
                    if "heartattack_Form" not in context:
                        context["heartattack_form"] = self.heartattack_form_class(
                            instance=self.medicalprofile.heartattack
                        )
                    if "CHF_form" not in context:
                        context["CHF_form"] = self.CHF_form_class(instance=self.medicalprofile.CHF)
                    if "stroke_form" not in context:
                        context["stroke_form"] = self.stroke_form_class(instance=self.medicalprofile.stroke)
                    if "PVD_form" not in context:
                        context["PVD_form"] = self.PVD_form_class(instance=self.medicalprofile.PVD)
                else:
                    get_blank_forms()
            else:
                get_blank_forms()
        else:
            get_blank_forms()
        return context

    def get_form_kwargs(self):
        """Overwrites get_form_kwargs() to look for 'gender' in kwargs
        Gender is set to the User object's PatientProfile gender
        Queries User PatientProfile
        returns: [dict: dict containing 'flare' kwarg for form]"""
        # Assign self.gender to None
        # Form won't error on loading from GET request kwargs
        # Before calling super() which will overwrite kwargs
        self.gender = None
        # Checks if user is logged in, if they have a patient profile gender, and if so, assign to self.gender
        if self.request.user.is_authenticated:
            if self.patientprofile:
                if self.patientprofile.gender:
                    self.gender = self.patientprofile.gender
        kwargs = super(FlareCreate, self).get_form_kwargs()
        # Pass self.gender to FlareForm as kwarg for use in form processing of male field
        if self.gender:
            kwargs["gender"] = self.gender
        return kwargs

    def get_object(self):
        object = self.model
        return object

    def get_success_url(self):
        if self.object.slug:
            return reverse("flare:user-detail", kwargs={"slug": self.object.slug})
        else:
            return reverse("flare:detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=Flare())
        urate_form = self.urate_form_class(request.POST, instance=Urate())
        # Assign related model forms to blank instances
        angina_form = self.angina_form_class(request.POST, instance=Angina())
        hypertension_form = self.hypertension_form_class(request.POST, instance=Hypertension())
        heartattack_form = self.heartattack_form_class(request.POST, instance=HeartAttack())
        CHF_form = self.CHF_form_class(request.POST, instance=CHF())
        stroke_form = self.stroke_form_class(request.POST, instance=Stroke())
        PVD_form = self.PVD_form_class(request.POST, instance=PVD())
        if request.user.is_authenticated:
            # If User is authenticated
            # Check if there is a User object
            if self.user and self.medicalprofile:
                angina_form = self.angina_form_class(request.POST, instance=self.medicalprofile.angina)
                hypertension_form = self.hypertension_form_class(
                    request.POST, instance=self.medicalprofile.hypertension
                )
                heartattack_form = self.heartattack_form_class(request.POST, instance=self.medicalprofile.heartattack)
                CHF_form = self.CHF_form_class(request.POST, instance=self.medicalprofile.CHF)
                stroke_form = self.stroke_form_class(request.POST, instance=self.medicalprofile.stroke)
                PVD_form = self.PVD_form_class(request.POST, instance=self.medicalprofile.PVD)
        if form.is_valid():
            flare_data = form.save(commit=False)
            if urate_form.is_valid():
                urate_data = urate_form.save(commit=False)
                if urate_data.value:
                    if self.user:
                        urate_data.user = self.user
                    urate_data.save()
                    flare_data.urate = urate_data
            if angina_form.is_valid():
                angina_data = angina_form.save(commit=False)
                angina_data.last_modified = "Flare"
                angina_data.save()
                flare_data.angina = angina_data
            if hypertension_form.is_valid():
                hypertension_data = hypertension_form.save(commit=False)
                hypertension_data.last_modified = "Flare"
                hypertension_data.save()
                flare_data.hypertension = hypertension_data
            if heartattack_form.is_valid():
                heartattack_data = heartattack_form.save(commit=False)
                heartattack_data.last_modified = "Flare"
                heartattack_data.save()
                flare_data.heartattack = heartattack_data
            if CHF_form.is_valid():
                CHF_data = CHF_form.save(commit=False)
                CHF_data.last_modified = "Flare"
                CHF_data.save()
                flare_data.CHF = CHF_data
            if stroke_form.is_valid():
                stroke_data = stroke_form.save(commit=False)
                stroke_data.last_modified = "Flare"
                stroke_data.save()
                flare_data.stroke = stroke_data
            if PVD_form.is_valid():
                PVD_data = PVD_form.save(commit=False)
                PVD_data.last_modified = "Flare"
                PVD_data.save()
                flare_data.PVD = PVD_data
            return self.form_valid(form)
        else:
            if request.user.is_authenticated:
                if self.user and self.medicalprofile:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            urate_form=self.urate_form_class(request.POST, instance=Urate()),
                            angina_form=self.angina_form_class(request.POST, instance=self.medicalprofile.angina),
                            hypertension_form=self.hypertension_form_class(
                                request.POST, instance=self.medicalprofile.hypertension
                            ),
                            heartattack_form=self.heartattack_form_class(
                                request.POST, instance=self.medicalprofile.heartattack
                            ),
                            CHF_form=self.CHF_form_class(request.POST, instance=self.medicalprofile.CHF),
                            stroke_form=self.stroke_form_class(request.POST, instance=self.medicalprofile.stroke),
                            PVD_form=self.PVD_form_class(request.POST, instance=self.medicalprofile.PVD),
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


class FlareUpdate(LoginRequiredMixin, PatientProviderMixin, UpdateView):
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
        if self.request.POST:
            if "urate_form" not in context:
                context["urate_form"] = self.urate_form_class(self.request.POST, instance=self.object.urate)
            if "angina_form" not in context:
                context["angina_form"] = self.angina_form_class(self.request.POST, instance=self.object.angina)
            if "hypertension_form" not in context:
                context["hypertension_form"] = self.hypertension_form_class(
                    self.request.POST, instance=self.object.hypertension
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    self.request.POST, instance=self.object.heartattack
                )
            if "CHF_form" not in context:
                context["CHF_form"] = self.CHF_form_class(self.request.POST, instance=self.object.CHF)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(self.request.POST, instance=self.object.stroke)
            if "PVD_form" not in context:
                context["PVD_form"] = self.PVD_form_class(self.request.POST, instance=self.object.PVD)
        else:
            if "urate_form" not in context:
                context["urate_form"] = self.urate_form_class(instance=self.object.urate)
            if "angina_form" not in context:
                context["angina_form"] = self.angina_form_class(instance=self.object.angina)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(instance=self.object.heartattack)
            if "hypertension_form" not in context:
                context["hypertension_form"] = self.hypertension_form_class(instance=self.object.hypertension)
            if "CHF_form" not in context:
                context["CHF_form"] = self.CHF_form_class(instance=self.object.CHF)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.object.stroke)
            if "PVD_form" not in context:
                context["PVD_form"] = self.PVD_form_class(instance=self.object.PVD)
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            flare_data = form.save(commit=False)
            urate_form = self.urate_form_class(request.POST, instance=self.object.urate)
            angina_form = self.angina_form_class(request.POST, instance=self.object.angina)
            hypertension_form = self.hypertension_form_class(request.POST, instance=self.object.hypertension)
            heartattack_form = self.heartattack_form_class(request.POST, instance=self.object.heartattack)
            CHF_form = self.CHF_form_class(request.POST, instance=self.object.CHF)
            stroke_form = self.stroke_form_class(request.POST, instance=self.object.stroke)
            PVD_form = self.PVD_form_class(request.POST, instance=self.object.PVD)
            if urate_form.is_valid():
                urate_data = urate_form.save(commit=False)
                # NEED TO DECIDE IF THIS IS HOW I WANT TO HANDLE A BLANK VALUE
                if urate_data.value:
                    urate_data.save()
                    flare_data.urate = urate_data
            if angina_form.is_valid():
                angina_data = angina_form.save(commit=False)
                angina_data.last_modified = "Flare"
                angina_data.save()
                flare_data.angina = angina_data
            if hypertension_form.is_valid():
                hypertension_data = hypertension_form.save(commit=False)
                hypertension_data.last_modified = "Flare"
                hypertension_data.save()
                flare_data.hypertension = hypertension_data
            if heartattack_form.is_valid():
                heartattack_data = heartattack_form.save(commit=False)
                heartattack_data.last_modified = "Flare"
                heartattack_data.save()
                flare_data.heartattack = heartattack_data
            if CHF_form.is_valid():
                CHF_data = CHF_form.save(commit=False)
                CHF_data.last_modified = "Flare"
                CHF_data.save()
                flare_data.CHF = CHF_data
            if stroke_form.is_valid():
                stroke_data = stroke_form.save(commit=False)
                stroke_data.last_modified = "Flare"
                stroke_data.save()
                flare_data.stroke = stroke_data
            if PVD_form.is_valid():
                PVD_data = PVD_form.save(commit=False)
                PVD_data.last_modified = "Flare"
                PVD_data.save()
                flare_data.PVD = PVD_data
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    urate_form=self.urate_form_class(request.POST, instance=self.object.urate),
                    angina_form=self.angina_form_class(request.POST, instance=self.object.angina),
                    hypertension_form=self.hypertension_form_class(request.POST, instance=self.object.hypertension),
                    heartattack_form=self.heartattack_form_class(request.POST, instance=self.object.heartattack),
                    CHF_form=self.CHF_form_class(request.POST, instance=self.object.CHF),
                    stroke_form=self.stroke_form_class(request.POST, instance=self.object.stroke),
                    PVD_form=self.PVD_form_class(request.POST, instance=self.object.PVD),
                )
            )
