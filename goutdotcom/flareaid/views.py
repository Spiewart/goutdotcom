from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..flare.forms import FlareForm
from ..flare.models import Flare
from ..history.forms import (
    AnticoagulationSimpleForm,
    BleedSimpleForm,
    CKDSimpleForm,
    ColchicineInteractionsSimpleForm,
    DiabetesSimpleForm,
    HeartAttackSimpleForm,
    IBDSimpleForm,
    OsteoporosisSimpleForm,
    StrokeSimpleForm,
)
from ..history.models import (
    CKD,
    IBD,
    Anticoagulation,
    Bleed,
    ColchicineInteractions,
    Diabetes,
    HeartAttack,
    Osteoporosis,
    Stroke,
)
from ..utils.mixins import (
    PatientProviderCreateMixin,
    PatientProviderListMixin,
    PatientProviderMixin,
    ProfileMixin,
    UserMixin,
    UserSlugMixin,
)
from .forms import FlareAidForm
from .mixins import FlareMixin
from .models import FlareAid


class FlareAidCreate(PatientProviderCreateMixin, FlareMixin, ProfileMixin, UserMixin, CreateView):
    """
    CreateView for FlareAids.
    Can take optional Flare kwarg, either PK or slug, to adjust the FlareAid fields/forms.
    Can be user-specific or not, depending on URL.
    Modifies related models via separate forms.
    Uses Mixins to avoid multiple queries (Flare, Profiles, User).
    Uses PatientProviderCreateMixin to restrict permissions.
    """

    # Set up form classes for get_context_data() and post() methods
    model = FlareAid
    form_class = FlareAidForm
    anticoagulation_form_class = AnticoagulationSimpleForm
    bleed_form_class = BleedSimpleForm
    CKD_form_class = CKDSimpleForm
    colchicine_interactions_form_class = ColchicineInteractionsSimpleForm
    diabetes_form_class = DiabetesSimpleForm
    flare_form_class = FlareForm
    heartattack_form_class = HeartAttackSimpleForm
    IBD_form_class = IBDSimpleForm
    osteoporosis_form_class = OsteoporosisSimpleForm
    stroke_form_class = StrokeSimpleForm

    def form_valid(self, form):
        """
        Checks if there is associated Flare
        Modifies FlareAid fields accordingly if so
        Sets form/object user via username kwarg
        Sets creator to request.user
        ***Requires FlareMixin, UserMixin***
        """
        # Check if POST has 'flare' kwarg
        # Assign FlareAid Flare OnetoOne related object based on pk/slug='flare'
        if self.flare:
            form.instance.flare = self.flare
            # Set monoarticular value based on Flare.monoarticular
            form.instance.monoarticular = form.instance.flare.monoarticular
            # If there isn't a User object associated with FlareAid --->
            # Use Flare HeartAttack and Stroke instances instead of making new ones
            # Removed forms in form via Kwargs and layout objects
            if not self.user:
                form.instance.heartattack = form.instance.flare.heartattack
                form.instance.stroke = form.instance.flare.stroke
        # If User is logged in, check if there is a User object associated with the new FlareAid
        # Uses UserMixin to set User and fetch from cache
        # If so, set form instance to that User
        if self.request.user.is_authenticated:
            if self.user:
                form.instance.user = self.user
            # Set creator to request.user
            form.instance.creator = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """Checks if Flare associated
        Checks if Flare has FlareAid and redirects to Detail if so
        Checks if FlareAid will have User via username kwarg
        Checks if FlareAid.user and Flare.user are the same
        Raises 404 if not
        ***Requires FlareMixin, UserMixin***
        """
        # Check if there is an associated flare
        if self.flare:
            # Check if that Flare has a FlareAid
            try:
                self.flareaid = self.flare.flareaid
            except FlareAid.DoesNotExist:
                self.flareaid = None
            # Redirect to FlareAid Detail if so
            if self.flareaid:
                if self.flare.flareaid.slug:
                    return redirect("flareaid:user-detail", slug=self.flareaid.slug)
                else:
                    return redirect("flareaid:detail", pk=self.flareaid.pk)
            # Check if User associated
            if self.user:
                # If so, check if Flare User and new object User are the same
                # Raise 404 if not
                if self.flare.user:
                    if self.flare.user != self.user:
                        raise PermissionDenied
                if not self.flare.user:
                    raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds related model forms to context
        If there is an associated User/MedicalProfile --->
        Pulls History objects from User's MedicalProfile
        Instantiates forms with related objects
        ***Requires UserMixin and ProfileMixin***
        """
        context = super(FlareAidCreate, self).get_context_data(**kwargs)

        # Function to set blank forms, DRY
        def get_blank_forms():
            if "anticoagulation_form" not in context:
                context["anticoagulation_form"] = self.anticoagulation_form_class(self.request.GET)
            if "bleed_form" not in context:
                context["bleed_form"] = self.bleed_form_class(self.request.GET)
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(self.request.GET)
            if "colchicine_interactions_form" not in context:
                context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(self.request.GET)
            if "diabetes_form" not in context:
                context["diabetes_form"] = self.diabetes_form_class(self.request.GET)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(self.request.GET)
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(self.request.GET)
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(self.request.GET)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(self.request.GET)

        # If the User is logged in, check if there is an associated User with a MedicalProfile
        if self.request.user.is_authenticated:
            # If so, set form instances to the MedicalProfile objects
            if self.medicalprofile:
                if "anticoagulation_form" not in context:
                    context["anticoagulation_form"] = self.anticoagulation_form_class(
                        instance=self.medicalprofile.anticoagulation
                    )
                if "bleed_form" not in context:
                    context["bleed_form"] = self.bleed_form_class(instance=self.medicalprofile.bleed)
                if "CKD_form" not in context:
                    context["CKD_form"] = self.CKD_form_class(instance=self.medicalprofile.CKD)
                if "colchicine_interactions_form" not in context:
                    context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                        instance=self.medicalprofile.colchicine_interactions
                    )
                if "diabetes_form" not in context:
                    context["diabetes_form"] = self.diabetes_form_class(instance=self.medicalprofile.diabetes)
                if "heartattack_form" not in context:
                    context["heartattack_form"] = self.heartattack_form_class(instance=self.medicalprofile.heartattack)
                if "IBD_form" not in context:
                    context["IBD_form"] = self.IBD_form_class(instance=self.medicalprofile.IBD)
                if "osteoporosis_form" not in context:
                    context["osteoporosis_form"] = self.osteoporosis_form_class(
                        instance=self.medicalprofile.osteoporosis
                    )
                if "stroke_form" not in context:
                    context["stroke_form"] = self.stroke_form_class(instance=self.medicalprofile.stroke)
            else:
                get_blank_forms()
        else:
            get_blank_forms()
        return context

    def get_form_kwargs(self):
        """
        Gets kwargs for form
        Look for 'flare' kwarg in GET request
        Uses 'flare' to query database for associated flare for use in FlareAidForm
        Adds cardiovascular diseases to form in order to modify form fields
        ***Requires FlareMixin and UserMixin***
        """
        kwargs = super(FlareAidCreate, self).get_form_kwargs()
        # Checks if flare kwarg came from Flare Detail and queries database for flare_pk that matches self.flare from initial kwargs
        # Add Flare's related models to the form for processing
        if self.flare:
            kwargs["flare"] = self.flare
            kwargs["angina"] = self.flare.angina
            kwargs["chf"] = self.flare.CHF
            kwargs["heartattack"] = self.flare.heartattack
            kwargs["hypertension"] = self.flare.hypertension
            kwargs["stroke"] = self.flare.stroke
            kwargs["pvd"] = self.flare.PVD
        # Pass whether or not there is a User to the form for processing
        if self.user:
            kwargs["no_user"] = False
        else:
            kwargs["no_user"] = True
        return kwargs

    def get_success_url(self):
        """
        Redirects to DetailView based on whether or not there is a slug
        PK if not
        """
        if self.object.slug:
            return reverse("flareaid:user-detail", kwargs={"slug": self.object.slug})
        else:
            return reverse("flareaid:detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        """
        Long multiform post() method to create FlareAid
        Modified related OnetoOne models from User's MedicalProfile
        ***Requires UserMixin and ProfileMixin***
        """
        ### Set form instances
        form = self.form_class(request.POST, instance=FlareAid())
        flareaid_data = form.save(commit=False)
        anticoagulation_form = self.anticoagulation_form_class(request.POST, instance=Anticoagulation())
        bleed_form = self.bleed_form_class(request.POST, instance=Bleed())
        CKD_form = self.CKD_form_class(request.POST, instance=CKD())
        colchicine_interactions_form = self.colchicine_interactions_form_class(
            request.POST, instance=ColchicineInteractions()
        )
        diabetes_form = self.diabetes_form_class(request.POST, instance=Diabetes())
        heartattack_form = self.heartattack_form_class(request.POST, instance=HeartAttack())
        IBD_form = self.IBD_form_class(request.POST, instance=IBD())
        osteoporosis_form = self.osteoporosis_form_class(request.POST, instance=Osteoporosis())
        stroke_form = self.stroke_form_class(request.POST, instance=Stroke())
        # If the User is logged in, if there is a User MedicalProfile object -->
        # Instantiate forms with History objects from MedicalProfile
        if request.user.is_authenticated:
            if self.medicalprofile:
                # Check there is a User with an associated MedicalProfile
                # Set form instances to MedicalProfile objects if so
                anticoagulation_form = self.anticoagulation_form_class(
                    request.POST, instance=self.medicalprofile.anticoagulation
                )
                bleed_form = self.bleed_form_class(request.POST, instance=self.medicalprofile.bleed)
                CKD_form = self.CKD_form_class(request.POST, instance=self.medicalprofile.CKD)
                colchicine_interactions_form = self.colchicine_interactions_form_class(
                    request.POST, instance=self.medicalprofile.colchicine_interactions
                )
                diabetes_form = self.diabetes_form_class(request.POST, instance=self.medicalprofile.diabetes)
                heartattack_form = self.heartattack_form_class(request.POST, instance=self.medicalprofile.heartattack)
                IBD_form = self.IBD_form_class(request.POST, instance=self.medicalprofile.IBD)
                osteoporosis_form = self.osteoporosis_form_class(
                    request.POST, instance=self.medicalprofile.osteoporosis
                )
                stroke_form = self.stroke_form_class(request.POST, instance=self.medicalprofile.stroke)
        if (
            form.is_valid()
            and anticoagulation_form.is_valid()
            and bleed_form.is_valid()
            and CKD_form.is_valid()
            and colchicine_interactions_form.is_valid()
            and diabetes_form.is_valid()
            and heartattack_form.is_valid()
            and IBD_form.is_valid()
            and osteoporosis_form.is_valid()
            and stroke_form.is_valid()
        ):
            # If forms valid, assign last_modified and save()
            anticoagulation_data = anticoagulation_form.save(commit=False)
            anticoagulation_data.last_modified = "FlareAid"
            anticoagulation_data.save()
            bleed_data = bleed_form.save(commit=False)
            bleed_data.last_modified = "FlareAid"
            bleed_data.save()
            ckd_data = CKD_form.save(commit=False)
            ckd_data.last_modified = "FlareAid"
            ckd_data.save()
            colchicine_interactions_data = colchicine_interactions_form.save(commit=False)
            colchicine_interactions_data.last_modified = "FlareAid"
            colchicine_interactions_data.save()
            diabetes_data = diabetes_form.save(commit=False)
            diabetes_data.last_modified = "FlareAid"
            diabetes_data.save()
            heartattack_data = heartattack_form.save(commit=False)
            heartattack_data.last_modified = "FlareAid"
            heartattack_data.save()
            IBD_data = IBD_form.save(commit=False)
            IBD_data.last_modified = "FlareAid"
            IBD_data.save()
            osteoporosis_data = osteoporosis_form.save(commit=False)
            osteoporosis_data.last_modified = "FlareAid"
            osteoporosis_data.save()
            stroke_data = stroke_form.save(commit=False)
            stroke_data.last_modified = "FlareAid"
            stroke_data.save()
            flareaid_data.anticoagulation = anticoagulation_data
            flareaid_data.bleed = bleed_data
            flareaid_data.ckd = ckd_data
            flareaid_data.colchicine_interactions = colchicine_interactions_data
            flareaid_data.diabetes = diabetes_data
            flareaid_data.heartattack = heartattack_data
            flareaid_data.ibd = IBD_data
            flareaid_data.osteoporosis = osteoporosis_data
            flareaid_data.stroke = stroke_data
            return self.form_valid(form)
        else:
            if request.user.is_authenticated:
                if self.medicalprofile:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            anticoagulation_form=self.anticoagulation_form_class(
                                request.POST, instance=self.medicalprofile.anticoagulation
                            ),
                            bleed_form=self.bleed_form_class(request.POST, instance=self.medicalprofile.bleed),
                            CKD_form=self.CKD_form_class(request.POST, instance=self.medicalprofile.CKD),
                            colchicine_interactions_form=self.colchicine_interactions_form_class(
                                request.POST, instance=self.medicalprofile.colchicine_interactions
                            ),
                            diabetes_form=self.diabetes_form_class(request.POST, instance=self.medicalprofile.diabetes),
                            heartattack_form=self.heartattack_form_class(
                                request.POST, instance=self.medicalprofile.heartattack
                            ),
                            IBD_form=self.IBD_form_class(request.POST, instance=self.medicalprofile.IBD),
                            osteoporosis_form=self.osteoporosis_form_class(
                                request.POST, instance=self.medicalprofile.osteoporosis
                            ),
                            stroke_form=self.stroke_form_class(request.POST, instance=self.medicalprofile.stroke),
                        )
                    )
                else:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            anticoagulation_form=self.anticoagulation_form_class(
                                request.POST, instance=Anticoagulation()
                            ),
                            bleed_form=self.bleed_form_class(request.POST, instance=Bleed()),
                            CKD_form=self.CKD_form_class(request.POST, instance=CKD()),
                            colchicine_interactions_form=self.colchicine_interactions_form_class(
                                request.POST, instance=ColchicineInteractions()
                            ),
                            diabetes_form=self.diabetes_form_class(request.POST, instance=Diabetes()),
                            heartattack_form=self.heartattack_form_class(request.POST, instance=HeartAttack()),
                            IBD_form=self.IBD_form_class(request.POST, instance=IBD()),
                            osteoporosis_form=self.osteoporosis_form_class(request.POST, instance=Osteoporosis()),
                            stroke_form=self.stroke_form_class(request.POST, instance=Stroke()),
                        )
                    )
            else:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        anticoagulation_form=self.anticoagulation_form_class(request.POST, instance=Anticoagulation()),
                        bleed_form=self.bleed_form_class(request.POST, instance=Bleed()),
                        CKD_form=self.CKD_form_class(request.POST, instance=CKD()),
                        colchicine_interactions_form=self.colchicine_interactions_form_class(
                            request.POST, instance=ColchicineInteractions()
                        ),
                        diabetes_form=self.diabetes_form_class(request.POST, instance=Diabetes()),
                        heartattack_form=self.heartattack_form_class(request.POST, instance=HeartAttack()),
                        IBD_form=self.IBD_form_class(request.POST, instance=IBD()),
                        osteoporosis_form=self.osteoporosis_form_class(request.POST, instance=Osteoporosis()),
                        stroke_form=self.stroke_form_class(request.POST, instance=Stroke()),
                    )
                )


class FlareAidDetail(PatientProviderMixin, DetailView):
    """
    FlareAid DetailView
    Takes PK or slug per the URL
    """

    model = FlareAid
    template_name = "flareaid/flareaid_detail.html"


class FlareAidList(LoginRequiredMixin, PatientProviderListMixin, ProfileMixin, UserMixin, ListView):
    """
    ListView for FlareAids
    Takes username kwarg to filter
    Users PatientProviderListMixin to limit view permission
    ***Requires PatientProviderListMixin and UserMixin***
    """

    model = FlareAid
    # Changed allow_empty to = False so it returns 404 when empty, then redirect with dispatch to DecisionAid About view
    allow_empty = False
    paginate_by = 5
    # Overrode dispatch to redirect to Flare About view if FlareAid view returns 404, as in the case of it being empty due to allow_empty=False

    def dispatch(self, *args, **kwargs):
        # If queryset is empty, redirect to flare:about instead of 404
        try:
            return super().dispatch(*args, **kwargs)
        except Http404:
            messages.info(self.request, f"No Flare Helpers to list!")
            return redirect("flare:about")

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        # Add modified queryset to context
        context.update(
            {
                "flareaid_list": FlareAid.objects.filter(user=self.user),
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # Limit queryset to User object via UserMixin
        return queryset.filter(user=self.user).order_by("-created")


class FlareAidUpdate(LoginRequiredMixin, PatientProviderMixin, ProfileMixin, UserSlugMixin, UpdateView):
    """
    Comparatively simple (relative to CreateView) UpdateView for FlareAid
    ***Requires PatientProviderMixin to limit permission***
    """

    # Set up form classes for subsequent models
    model = FlareAid
    form_class = FlareAidForm
    anticoagulation_form_class = AnticoagulationSimpleForm
    bleed_form_class = BleedSimpleForm
    CKD_form_class = CKDSimpleForm
    colchicine_interactions_form_class = ColchicineInteractionsSimpleForm
    diabetes_form_class = DiabetesSimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    IBD_form_class = IBDSimpleForm
    osteoporosis_form_class = OsteoporosisSimpleForm
    stroke_form_class = StrokeSimpleForm

    def form_valid(self, form):
        """
        If there is an associated Flare --->
        Assign Flare.monoarticular to FlareAid's
        ***Requires FlareMixin***
        """
        # Check if POST has 'flare' kwarg via UserSlugMixin
        # Assign Flare.monoarticular to FlareAid.monoarticular if so
        if self.flare:
            form.instance.monoarticular = form.instance.flare.monoarticular
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Instantiates related model forms with model instances
        """
        context = super(FlareAidUpdate, self).get_context_data(**kwargs)
        # Add related model forms with instances
        if self.request.POST:
            if "anticoagulation_form" not in context:
                context["anticoagulation_form"] = self.anticoagulation_form_class(
                    self.request.POST, instance=self.object.anticoagulation
                )
            if "bleed_form" not in context:
                context["bleed_form"] = self.bleed_form_class(self.request.POST, instance=self.object.bleed)
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(self.request.POST, instance=self.object.ckd)
            if "colchicine_interactions_form" not in context:
                context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                    self.request.POST, instance=self.object.colchicine_interactions
                )
            if "diabetes_form" not in context:
                context["diabetes_form"] = self.diabetes_form_class(self.request.POST, instance=self.object.diabetes)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    self.request.POST, instance=self.object.heartattack
                )
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(self.request.POST, instance=self.object.ibd)
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(
                    self.request.POST, instance=self.object.osteoporosis
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(self.request.POST, instance=self.object.stroke)
        else:
            if "anticoagulation_form" not in context:
                context["anticoagulation_form"] = self.anticoagulation_form_class(instance=self.object.anticoagulation)
            if "bleed_form" not in context:
                context["bleed_form"] = self.bleed_form_class(instance=self.object.bleed)
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.object.ckd)
            if "colchicine_interactions_form" not in context:
                context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                    instance=self.object.colchicine_interactions
                )
            if "diabetes_form" not in context:
                context["diabetes_form"] = self.diabetes_form_class(instance=self.object.diabetes)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(instance=self.object.heartattack)
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(instance=self.object.ibd)
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(instance=self.object.osteoporosis)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.object.stroke)
        return context

    def get_form_kwargs(self):
        """
        Looks for Flare related object via kwargs and FlareMixin
        Uses 'flare' to query database for associated flare for use in FlareAidForm
        Adds cardiovascular diseases to form in order to modify form fields
        ***Requires FlareMixin***
        """
        # Call super() first because it overwrites kwargs
        kwargs = super(FlareAidUpdate, self).get_form_kwargs()
        # Checks if flare kwarg came from Flare Detail
        if self.flare:
            # Assigns cardiovascular diseases to kwargs for form processing
            kwargs["flare"] = self.flare
            kwargs["angina"] = self.flare.angina
            kwargs["chf"] = self.flare.CHF
            kwargs["heartattack"] = self.flare.heartattack
            kwargs["hypertension"] = self.flare.hypertension
            kwargs["stroke"] = self.flare.stroke
            kwargs["pvd"] = self.flare.PVD
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        Long multiform post() method to update FlareAids
        """
        # Uses get_object() to get the FlareAid instance requested and put it in a form
        self.object = self.get_object()
        # Assign forms for object and related models
        form = self.form_class(request.POST, instance=self.get_object())
        anticoagulation_form = self.anticoagulation_form_class(request.POST, instance=self.object.anticoagulation)
        bleed_form = self.bleed_form_class(request.POST, instance=self.object.bleed)
        CKD_form = self.CKD_form_class(request.POST, instance=self.object.ckd)
        colchicine_interactions_form = self.colchicine_interactions_form_class(
            request.POST, instance=self.object.colchicine_interactions
        )
        diabetes_form = self.diabetes_form_class(request.POST, instance=self.object.diabetes)
        heartattack_form = self.heartattack_form_class(request.POST, instance=self.object.heartattack)
        IBD_form = self.IBD_form_class(request.POST, instance=self.object.ibd)
        osteoporosis_form = self.osteoporosis_form_class(request.POST, instance=self.object.osteoporosis)
        stroke_form = self.stroke_form_class(request.POST, instance=self.object.stroke)

        # If forms are valid, modify last_modified and save()
        if form.is_valid():
            flareaid_data = form.save(commit=False)
            if anticoagulation_form.is_valid():
                anticoagulation_data = anticoagulation_form.save(commit=False)
                anticoagulation_data.last_modified = "FlareAid"
                anticoagulation_data.save()
                flareaid_data.anticoagulation = anticoagulation_data
            if bleed_form.is_valid():
                bleed_data = bleed_form.save(commit=False)
                bleed_data.last_modified = "FlareAid"
                bleed_data.save()
                flareaid_data.bleed = bleed_data
            if CKD_form.is_valid():
                ckd_data = CKD_form.save(commit=False)
                ckd_data.last_modified = "FlareAid"
                ckd_data.save()
                flareaid_data.ckd = ckd_data
            if colchicine_interactions_form.is_valid():
                colchicine_interactions_data = colchicine_interactions_form.save(commit=False)
                colchicine_interactions_data.last_modified = "FlareAid"
                colchicine_interactions_data.save()
                flareaid_data.colchicine_interactions = colchicine_interactions_data
            if diabetes_form.is_valid():
                diabetes_data = diabetes_form.save(commit=False)
                diabetes_data.last_modified = "FlareAid"
                diabetes_data.save()
                flareaid_data.diabetes = diabetes_data
            if heartattack_form.is_valid():
                heartattack_data = heartattack_form.save(commit=False)
                heartattack_data.last_modified = "FlareAid"
                heartattack_data.save()
                flareaid_data.heartattack = heartattack_data
            if IBD_form.is_valid():
                IBD_data = IBD_form.save(commit=False)
                IBD_data.last_modified = "FlareAid"
                IBD_data.save()
                flareaid_data.ibd = IBD_data
            if osteoporosis_form.is_valid():
                osteoporosis_data = osteoporosis_form.save(commit=False)
                osteoporosis_data.last_modified = "FlareAid"
                osteoporosis_data.save()
                flareaid_data.osteoporosis = osteoporosis_data
            if stroke_form.is_valid():
                stroke_data = stroke_form.save(commit=False)
                stroke_data.last_modified = "FlareAid"
                stroke_data.save()
                flareaid_data.stroke = stroke_data
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    anticoagulation_form=self.anticoagulation_form_class(
                        request.POST, instance=self.object.anticoagulation
                    ),
                    bleed_form=self.bleed_form_class(request.POST, instance=self.object.bleed),
                    CKD_form=self.CKD_form_class(request.POST, instance=self.object.ckd),
                    colchicine_interactions_form=self.colchicine_interactions_form_class(
                        request.POST, instance=self.object.colchicine_interactions
                    ),
                    diabetes_form=self.diabetes_form_class(request.POST, instance=self.object.diabetes),
                    heartattack_form=self.heartattack_form_class(request.POST, instance=self.object.heartattack),
                    IBD_form=self.IBD_form_class(request.POST, instance=self.object.ibd),
                    osteoporosis_form=self.osteoporosis_form_class(request.POST, instance=self.object.osteoporosis),
                    stroke_form=self.stroke_form_class(request.POST, instance=self.object.stroke),
                )
            )
