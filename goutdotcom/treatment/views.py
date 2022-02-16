from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from goutdotcom.treatment.choices import COLCHICINE

from ..flareaid.models import FlareAid
from ..ppxaid.models import PPxAid
from ..utils.mixins import (
    PatientProviderCreateMixin,
    PatientProviderListMixin,
    PatientProviderMixin,
    ProfileMixin,
    TreatmentModelMixin,
    UserMixin,
    UserSlugMixin,
)
from .forms import *
from .models import (
    Allopurinol,
    Celecoxib,
    Colchicine,
    Febuxostat,
    Ibuprofen,
    Meloxicam,
    Methylprednisolone,
    Naproxen,
    Othertreat,
    Prednisone,
    Probenecid,
    Tinctureoftime,
)

non_prn_models = [Allopurinol, Febuxostat, Probenecid]
allopurinol_model = [Allopurinol]
prn_models = [
    Colchicine,
    Ibuprofen,
    Indomethacin,
    Naproxen,
    Meloxicam,
    Celecoxib,
    Prednisone,
    Methylprednisolone,
    Tinctureoftime,
    Othertreat,
]
injection_models = [Methylprednisolone]

### About views ###
class About(TemplateView):
    template_name = "treatment/about.html"


class AboutCorticosteroids(TemplateView):
    template_name = "treatment/about_corticosteroids.html"


class AboutFlare(TemplateView):
    template_name = "treatment/about_flare.html"


class AboutNSAIDs(TemplateView):
    template_name = "treatment/about_NSAIDs.html"


class AboutProphylaxis(TemplateView):
    template_name = "treatment/about_prophylaxis.html"


class AboutULT(TemplateView):
    template_name = "treatment/about_ult.html"


class TreatmentAbout(TemplateView):
    """Dynamic treatment-specific About view.
    Takes treatment kwarg, fetches appropriate template with it
    """

    def get_template_names(self, **kwargs):
        kwargs = self.kwargs
        treatment = kwargs.get("treatment")
        template = "treatment/" + str(treatment) + "_about.html"
        return template

    def get_context_data(self, **kwargs):
        context = super(TreatmentAbout, self).get_context_data(**kwargs)
        context.update(
            {
                "treatment": self.kwargs["treatment"],
            }
        )
        return context


class IndexView(LoginRequiredMixin, PatientProviderListMixin, ProfileMixin, UserMixin, ListView):
    """View to display all a User's treatment.
    Takes username kwarg, uses Profile/UserMixin.
    PatientProviderListMixin for permission.
    """

    template_name = "treatment/index.html"
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            {
                "allopurinol_list": Allopurinol.objects.filter(user=self.user),
                "febuxostat_list": Febuxostat.objects.filter(user=self.user),
                "colchicine_list": Colchicine.objects.filter(user=self.user, as_prophylaxis=False).order_by("-created")[
                    :1
                ],
                "ibuprofen_list": Ibuprofen.objects.filter(user=self.user, as_prophylaxis=False).order_by("-created")[
                    :1
                ],
                "celecoxib_list": Celecoxib.objects.filter(user=self.user, as_prophylaxis=False).order_by("-created")[
                    :1
                ],
                "meloxicam_list": Meloxicam.objects.filter(user=self.user, as_prophylaxis=False).order_by("-created")[
                    :1
                ],
                "naproxen_list": Naproxen.objects.filter(user=self.user, as_prophylaxis=False).order_by("-created")[:1],
                "prednisone_list": Prednisone.objects.filter(user=self.user, as_prophylaxis=False).order_by("-created")[
                    :1
                ],
                "probenecid_list": Probenecid.objects.filter(user=self.user),
                "methylprednisolone_list": Methylprednisolone.objects.filter(user=self.user).order_by("-created")[:1],
                "colchicine_ppx_list": Colchicine.objects.filter(user=self.user, as_prophylaxis=True)[:1],
                "ibuprofen_ppx_list": Ibuprofen.objects.filter(user=self.user, as_prophylaxis=True)[:1],
                "celecoxib_ppx_list": Celecoxib.objects.filter(user=self.user, as_prophylaxis=True)[:1],
                "meloxicam_ppx_list": Meloxicam.objects.filter(user=self.user, as_prophylaxis=True)[:1],
                "naproxen_ppx_list": Naproxen.objects.filter(user=self.user, as_prophylaxis=True)[:1],
                "prednisone_ppx_list": Prednisone.objects.filter(user=self.user, as_prophylaxis=True)[:1],
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.user)


class FlareView(LoginRequiredMixin, PatientProviderListMixin, UserMixin, ListView):
    template_name = "treatment/flare.html"
    model = Colchicine

    def get_context_data(self, **kwargs):
        context = super(FlareView, self).get_context_data(**kwargs)
        context.update(
            {
                "colchicine_list": Colchicine.objects.filter(user=self.user, as_prophylaxis=False),
                "ibuprofen_list": Ibuprofen.objects.filter(user=self.user, as_prophylaxis=False),
                "celecoxib_list": Celecoxib.objects.filter(user=self.user, as_prophylaxis=False),
                "meloxicam_list": Meloxicam.objects.filter(user=self.user, as_prophylaxis=False),
                "naproxen_list": Naproxen.objects.filter(user=self.user, as_prophylaxis=False),
                "prednisone_list": Prednisone.objects.filter(user=self.user, as_prophylaxis=False),
                "methylprednisolone_list": Methylprednisolone.objects.filter(user=self.user, as_injection=True),
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.user)


class ProphylaxisView(LoginRequiredMixin, PatientProviderListMixin, UserMixin, ListView):
    """For creating prophylactic therapy medication objects. The model field as_prophylaxis is switched to True with form.is_valid(). I had to create a new view rather than inherit from TreatmentCreate because of form.is_valid() super inheritance. It also let me rewrite some of the form fields rendered, such as prn."""

    template_name = "treatment/prophylaxis.html"
    model = Colchicine

    def get_context_data(self, **kwargs):
        context = super(ProphylaxisView, self).get_context_data(**kwargs)
        context.update(
            {
                "lists": {
                    "colchicine_ppx_list": Colchicine.objects.filter(user=self.user, as_prophylaxis=True),
                    "ibuprofen_ppx_list": Ibuprofen.objects.filter(user=self.user, as_prophylaxis=True),
                    "celecoxib_ppx_list": Celecoxib.objects.filter(user=self.user, as_prophylaxis=True),
                    "meloxicam_ppx_list": Meloxicam.objects.filter(user=self.user, as_prophylaxis=True),
                    "naproxen_ppx_list": Naproxen.objects.filter(user=self.user, as_prophylaxis=True),
                    "prednisone_ppx_list": Prednisone.objects.filter(user=self.user, as_prophylaxis=True),
                },
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.user)


class ULTView(LoginRequiredMixin, PatientProviderListMixin, UserMixin, ListView):
    template_name = "treatment/ult.html"
    model = Allopurinol

    def get_context_data(self, **kwargs):
        context = super(ULTView, self).get_context_data(**kwargs)
        context.update(
            {
                "lists": {
                    "allopurinol_list": Allopurinol.objects.filter(user=self.user),
                    "febuxostat_list": Febuxostat.objects.filter(user=self.user),
                    "probenecid_list": Probenecid.objects.filter(user=self.user),
                },
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.user)


class ProphylaxisCreate(LoginRequiredMixin, PatientProviderCreateMixin, UserMixin, TreatmentModelMixin, CreateView):
    fields = ["dose", "freq", "side_effects"]

    def get_form_class(self):
        if self.model in prn_models:
            self.fields.append("date_started")
            self.fields.append("date_ended")
        return modelform_factory(self.model, fields=self.fields)

    def get_template_names(self):
        template = "treatment/prophylaxis_form.html"
        return template

    def form_valid(self, form):
        form.instance.user = self.user
        form.instance.creator = self.request.user
        form.instance.as_prophylaxis = True
        form.instance.prn = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProphylaxisCreate, self).get_context_data(**kwargs)
        context.update(
            {
                "treatment": self.kwargs["treatment"],
            }
        )
        return context


class FlareAidTreatmentCreate(LoginRequiredMixin, PatientProviderCreateMixin, UserMixin, TreatmentModelMixin, View):
    def post(self, request, *args, **kwargs):
        self.flareaid = FlareAid.objects.get(slug=self.kwargs["slug"])
        self.model(user=self.user, creator=self.request.user, flareaid=self.flareaid).save()
        return HttpResponseRedirect(reverse("flareaid:user-detail", kwargs={"slug": self.kwargs["slug"]}))


class TreatmentCreate(
    LoginRequiredMixin, PatientProviderCreateMixin, ProfileMixin, UserMixin, TreatmentModelMixin, CreateView
):
    """Generic Treatment CreateView.
    URL parameters:
    treatment specifying which Treatment to create
    username to attach a User object to the Treatment object

    Returns:
        redirect: DetailView for newly created Treatment
    """

    fields = ["dose", "freq", "side_effects"]

    def get(self, request, *args, **kwargs):
        # Model fetched from TreatmentModelMixin cached_property
        self.object = None
        # Check if Treatment model is one that a User can only have a single instance of
        if self.model in non_prn_models:
            # If so, redirect User to UpdateView if they already have an instance of that treatment
            # Mainly meant for ULT treatments
            try:
                user_treatment = self.model.objects.get(user=self.user)
            except self.model.DoesNotExist:
                user_treatment = None
            if user_treatment:
                return redirect(
                    "treatment:update",
                    treatment=self.kwargs["treatment"],
                    slug=self.model.objects.get(user=self.user).slug,
                )
        return super().get(request, *args, **kwargs)

    def get_form_class(self, *args, **kwargs):
        # Add fields to form based on what Treatment model is
        # Model fetched from TreatmentModelMixin cached_property
        if self.model in prn_models:
            self.fields.append("prn")
        if self.model in allopurinol_model:
            self.fields.append("de_sensitized")
        if self.model in injection_models:
            self.fields.append("as_injection")
        return modelform_factory(self.model, fields=self.fields)

    def get_template_names(self):
        template = "treatment/treatment_form.html"
        return template

    def form_valid(self, form):
        # Assign model user from UserMixin
        form.instance.user = self.user
        # Assign creator to logged in User
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # WHY REWRITE THIS?
        context = super(TreatmentCreate, self).get_context_data(**kwargs)
        context.update(
            {
                "treatment": self.kwargs["treatment"],
            }
        )
        return context


class TreatmentDetail(LoginRequiredMixin, PatientProviderMixin, UserSlugMixin, DetailView):
    def get_object(self):
        self.model = apps.get_model("treatment", model_name=self.kwargs["treatment"])
        if self.kwargs.get("pk"):
            treatment = get_object_or_404(self.model, pk=self.kwargs["pk"])
        else:
            treatment = get_object_or_404(self.model, slug=self.kwargs["slug"])
        return treatment

    def get_template_names(self):
        template = "treatment/treatment_detail.html"
        return template


class TreatmentList(
    LoginRequiredMixin, PatientProviderListMixin, ProfileMixin, UserMixin, TreatmentModelMixin, ListView
):
    paginate_by = 5

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.filter(user=self.user).order_by("-created")
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
                )
        return self.queryset.filter(user=self.user).order_by("-created")

    def get_template_names(self):
        template = "treatment/treatment_list.html"
        return template

    def get_context_data(self, **kwargs):
        context = super(TreatmentList, self).get_context_data(**kwargs)
        context.update(
            {
                "treatment": self.kwargs["treatment"],
            }
        )
        return context


class TreatmentUpdate(
    LoginRequiredMixin, PatientProviderMixin, ProfileMixin, UserMixin, TreatmentModelMixin, UpdateView
):
    fields = [
        "dose",
        "freq",
        "side_effects",
        "prn",
        "date_started",
        "date_ended",
        "de_sensitized",
        "as_injection",
    ]

    def get_form_class(self):
        if self.form_class:
            if self.model not in prn_models:
                if "prn" in self.fields:
                    self.fields.remove("prn")
                if "date_started" in self.fields:
                    self.fields.remove("date_started")
                if "date_ended" in self.fields:
                    self.fields.remove("date_ended")
            if self.model not in allopurinol_model:
                if "de_sensitized" in self.fields:
                    self.fields.remove("de_sensitized")
            if self.model not in injection_models:
                if "as_injection" in self.fields:
                    self.fields.remove("as_injection")
            return self.form_class
        else:
            if self.model not in prn_models:
                if "prn" in self.fields:
                    self.fields.remove("prn")
                if "date_started" in self.fields:
                    self.fields.remove("date_started")
                if "date_ended" in self.fields:
                    self.fields.remove("date_ended")
            if self.model not in allopurinol_model:
                if "de_sensitized" in self.fields:
                    self.fields.remove("de_sensitized")
            if self.model not in injection_models:
                if "as_injection" in self.fields:
                    self.fields.remove("as_injection")
            return modelform_factory(self.model, fields=self.fields)

    def get_template_names(self):
        template = "treatment/treatment_form.html"
        return template

    def get_context_data(self, **kwargs):
        context = super(TreatmentUpdate, self).get_context_data(**kwargs)
        context.update(
            {
                "treatment": self.kwargs["treatment"],
            }
        )
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        try:
            queryset = self.model.objects.filter(slug=slug)
        except self.model.DoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(TreatmentUpdate, self).get_object(queryset=queryset)
        return obj
