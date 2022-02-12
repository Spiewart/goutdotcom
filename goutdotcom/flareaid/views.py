from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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
    PatientProviderMixin,
    ProfileMixin,
    UserMixin,
)
from .forms import FlareAidForm
from .models import FlareAid


class FlareAidCreate(PatientProviderCreateMixin, ProfileMixin, UserMixin, CreateView):
    ### NEED TO WRITE REDIRECT IF FLAREAID ALREADY EXISTS FOR FLARE ==> UPDATE
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
        # Check if POST has 'flare' kwarg and assign FlareAid Flare OnetoOne related object based on pk='flare'
        if self.kwargs.get("flare"):
            form.instance.flare = Flare.objects.get(pk=self.kwargs.get("flare"))
            form.instance.monoarticular = form.instance.flare.monoarticular
            # If user is not authenticated and created a FlareAid from a Flare --->
            # Use Flare HeartAttack and Stroke instances instead of making new ones
            # Removed forms in form via Kwargs and layout objects
            if self.request.user.is_authenticated == False:
                form.instance.heartattack = form.instance.flare.heartattack
                form.instance.stroke = form.instance.flare.stroke
        # If user is logged in, check if there is a User object associated with the new FlareAid
        # Uses UserMixin to set User and fetch from cache
        # If so, set form instance to that User
        if self.request.user.is_authenticated:
            if self.user:
                form.instance.user = self.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FlareAidCreate, self).get_context_data(**kwargs)

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
        """Ovewrites get_form_kwargs() to look for 'flare' kwarg in GET request
        Uses 'flare' to query database for associated flare for use in FlareAidForm
        returns: [dict: dict containing 'flare' kwarg for form]
        """
        # Assign self.flare from GET request kwargs before calling super() which will overwrite kwargs
        self.flare = self.kwargs.get("flare", None)
        self.no_user = False
        # Check if there is no User associated with the form
        # Set no_user appropriately for use in form rendering
        if not self.user:
            self.no_user = True
        kwargs = super(FlareAidCreate, self).get_form_kwargs()
        # Checks if flare kwarg came from Flare Detail and queries database for flare_pk that matches self.flare from initial kwargs
        if self.flare:
            flare_pk = self.flare
            flare = Flare.objects.get(pk=flare_pk)
            # Pass flare and no_user to form
            kwargs["flare"] = flare
            kwargs["no_user"] = self.no_user
            # If User is anonymous / not logged in and FlareAid has a Flare -->
            # Pass stroke and heartattack from Flare to FlareAid to avoid duplication of user input
            if self.no_user:
                kwargs["stroke"] = flare.stroke
                kwargs["heartattack"] = flare.heartattack
        return kwargs

    def get_success_url(self):
        if self.object.slug:
            return reverse("flareaid:user-detail", kwargs={"slug": self.object.slug})
        else:
            return reverse("flareaid:detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
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
    model = FlareAid
    template_name = "flareaid/flareaid_detail.html"


class FlareAidList(LoginRequiredMixin, UserMixin, ListView):
    model = FlareAid
    """Changed allow_empty to = False so it returns 404 when empty, then redirect with dispatch to DecisionAid About view"""

    allow_empty = False
    paginate_by = 5
    """Overrode dispatch to redirect to Flare About view if FlareAid view returns 404, as in the case of it being empty due to allow_empty=False
    """

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Http404:
            messages.info(self.request, f"No Flare Helpers to list!")
            return redirect("flare:about")

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update(
            {
                "flareaid_list": FlareAid.objects.filter(user=self.user),
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.user).order_by("-created")


class FlareAidUpdate(LoginRequiredMixin, PatientProviderMixin, UpdateView):
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
        # Check if POST has 'flare' kwarg
        # Assign FlareAid Flare OnetoOne related object based on pk='flare' or
        self.flare = self.kwargs.get("flare", None)
        if self.flare:
            if isinstance(self.flare, int):
                form.instance.flare = get_object_or_404(Flare, pk=self.flare)
            else:
                form.instance.flare = get_object_or_404(Flare, slug=self.flare)
            form.instance.monoarticular = form.instance.flare.monoarticular
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FlareAidUpdate, self).get_context_data(**kwargs)
        # Add related model forms with instances
        if self.request.POST:
            if "anticoagulation_form" not in context:
                context["anticoagulation_form"] = self.anticoagulation_form_class(
                    self.request.POST, instance=self.object.anticoagulation
                )
            if "bleed_form" not in context:
                context["bleed_form"] = self.bleed_form_class(
                    self.request.POST, instance=self.object.bleed
                )
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(
                    self.request.POST, instance=self.object.CKD
                )
            if "colchicine_interactions_form" not in context:
                context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                    self.request.POST, instance=self.object.colchicine_interactions
                )
            if "diabetes_form" not in context:
                context["diabetes_form"] = self.diabetes_form_class(
                    self.request.POST, instance=self.object.diabetes
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    self.request.POST, instance=self.object.heartattack
                )
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(
                    self.request.POST, instance=self.object.IBD
                )
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(
                    self.request.POST, instance=self.object.osteoporosis
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(
                    self.request.POST, instance=self.object.stroke
                )
        else:
            if "anticoagulation_form" not in context:
                context["anticoagulation_form"] = self.anticoagulation_form_class(
                    instance=self.object.anticoagulation
                )
            if "bleed_form" not in context:
                context["bleed_form"] = self.bleed_form_class(instance=self.object.bleed)
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.object.CKD)
            if "colchicine_interactions_form" not in context:
                context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                    instance=self.object.colchicine_interactions
                )
            if "diabetes_form" not in context:
                context["diabetes_form"] = self.diabetes_form_class(instance=self.object.diabetes)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    instance=self.object.heartattack
                )
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(instance=self.object.IBD)
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(
                    instance=self.object.osteoporosis
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.object.stroke)
        return context

    def get_form_kwargs(self):
        """Ovewrites get_form_kwargs() to look for 'flare' kwarg in GET request, uses 'flare' to query database for associated flare for use in FlareAidForm
        returns: [dict: dict containing 'flare' kwarg for form]"""
        # Assign self.flare from GET request kwargs before calling super() which will overwrite kwargs
        self.flare = self.kwargs.get("flare", None)
        kwargs = super(FlareAidUpdate, self).get_form_kwargs()
        # Checks if flare kwarg came from Flare Detail
        # Try to get Flare based on pk or slug
        # Return in kwargs if found, 404 otherwise
        if self.flare:
            flare = None
            if isinstance(self.flare, int):
                flare = get_object_or_404(Flare, pk=self.flare)
            else:
                flare = get_object_or_404(Flare, slug=self.flare)
            kwargs["heartattack"] = flare.heartattack
            kwargs["stroke"] = flare.stroke
            kwargs["flare"] = flare
        return kwargs

    def post(self, request, *args, **kwargs):
        # Uses UpdateView to get the FlareAid instance requested and put it in a form
        form = self.form_class(request.POST, instance=self.get_object())
        anticoagulation_form = self.anticoagulation_form_class(
            request.POST, instance=self.object.anticoagulation
        )
        bleed_form = self.bleed_form_class(request.POST, instance=self.object.bleed)
        CKD_form = self.CKD_form_class(request.POST, instance=self.object.CKD)
        colchicine_interactions_form = self.colchicine_interactions_form_class(
            request.POST, instance=self.object.colchicine_interactions
        )
        diabetes_form = self.diabetes_form_class(request.POST, instance=self.object.diabetes)
        heartattack_form = self.heartattack_form_class(request.POST, instance=self.object.heartattack)
        IBD_form = self.IBD_form_class(request.POST, instance=self.object.IBD)
        osteoporosis_form = self.osteoporosis_form_class(
            request.POST, instance=self.object.osteoporosis
        )
        stroke_form = self.stroke_form_class(request.POST, instance=self.object.stroke)

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
                    CKD_form=self.CKD_form_class(request.POST, instance=self.object.CKD),
                    colchicine_interactions_form=self.colchicine_interactions_form_class(
                        request.POST, instance=self.object.colchicine_interactions
                    ),
                    diabetes_form=self.diabetes_form_class(request.POST, instance=self.object.diabetes),
                    heartattack_form=self.heartattack_form_class(
                        request.POST, instance=self.object.heartattack
                    ),
                    IBD_form=self.IBD_form_class(request.POST, instance=self.object.IBD),
                    osteoporosis_form=self.osteoporosis_form_class(
                        request.POST, instance=self.object.osteoporosis
                    ),
                    stroke_form=self.stroke_form_class(request.POST, instance=self.object.stroke),
                )
            )
