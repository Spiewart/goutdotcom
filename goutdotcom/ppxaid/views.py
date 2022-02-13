from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from ..history.forms import (
    AnticoagulationSimpleForm,
    BleedSimpleForm,
    CKDForm,
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
from ..ultaid.models import ULTAid
from ..utils.mixins import (
    PatientProviderCreateMixin,
    PatientProviderMixin,
    ProfileMixin,
    UserMixin,
)
from .forms import PPxAidForm
from .models import PPxAid

User = get_user_model()


class PPxAidCreate(PatientProviderCreateMixin, ProfileMixin, SuccessMessageMixin, UserMixin, CreateView):
    model = PPxAid
    form_class = PPxAidForm
    anticoagulation_form_class = AnticoagulationSimpleForm
    bleed_form_class = BleedSimpleForm
    CKD_form_class = CKDForm
    colchicine_interactions_form_class = ColchicineInteractionsSimpleForm
    diabetes_form_class = DiabetesSimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    IBD_form_class = IBDSimpleForm
    osteoporosis_form_class = OsteoporosisSimpleForm
    stroke_form_class = StrokeSimpleForm

    def form_valid(self, form):
        # Check if POST has 'ultaid' kwarg and assign PPxAid OnetoOne related object based on pk or slug (username)
        if self.kwargs.get("ultaid"):
            if isinstance(self.kwargs.get("ultaid"), int):
                form.instance.ultaid = get_object_or_404(ULTAid, pk=self.kwargs.get("ultaid"))
            elif isinstance(self.kwargs.get("ultaid"), str):
                form.instance.ultaid = get_object_or_404(ULTAid, slug=self.kwargs.get("ultaid"))
            # If user is not authenticated and created a PPxAid from a ULTAid, use ULTAid CKD, HeartAttack, and Stroke instances instead of making new ones, removed forms in form via Kwargs and layout objects
            if self.request.user.is_authenticated == False:
                form.instance.ckd = form.instance.ultaid.ckd
                form.instance.heartattack = form.instance.ultaid.heartattack
                form.instance.stroke = form.instance.ultaid.stroke
        # If User is authenticated, check if Provider or Patient
        if self.request.user.is_authenticated:
            # Assign new object user to self.user via UserMixin
            form.instance.user = self.user
            # Set new object creator to request.user
            form.instance.creator = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Checks if User is authenticated and redirects to PPxAid UpdateView if so
        # Check for ultaid kwarg, fetch ultaid if so
        self.ultaid_index = self.kwargs.get("ultaid", None)
        self.ultaid = None

        if self.ultaid_index:
            if isinstance(self.ultaid_index, str):
                self.ultaid = get_object_or_404(ULTAid, slug=self.ultaid_index)
            else:
                self.ultaid = get_object_or_404(ULTAid, pk=self.ultaid_index)

        # Check if there is a User and ULTAid via user and ultaid kwargs
        # If those users are not the same, raise PermissionDenied
        # Blocks modifying another User's ULTAid instance via PPxAidCreate
        if self.user and self.ultaid:
            if self.ultaid.user:
                if self.ultaid.user != self.user:
                    raise PermissionDenied
            if not self.ultaid.user:
                raise PermissionDenied

        if self.request.user.is_authenticated:
            user_PPxAid = None
            if "username" in kwargs:
                try:
                    user_PPxAid = self.model.objects.get(slug=self.kwargs.get("username"))
                except self.model.DoesNotExist:
                    user_PPxAid = None
            if user_PPxAid:
                return redirect("ppxaid:user-detail", slug=user_PPxAid.slug)
        else:
            # If User not logged in, check if there is a ultaid in kwargs
            # Check if that ultaid already has a PPxAid, redirect if so
            if self.ultaid:
                try:
                    ultaid_PPxAid = self.model.objects.get(ultaid=self.ultaid)
                except self.model.DoesNotExist:
                    ultaid_PPxAid = None
                if ultaid_PPxAid:
                    return redirect("ppxaid:detail", pk=self.ultaid.ppxaid.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Overwritten to check if the User is logged in
        Checks if there is a username kwarg supplied
        Check if there is a User associated with username kwarg
        Passes to generate blank form if not

        Returns:
            [dict]: [context]
        """
        context = super(PPxAidCreate, self).get_context_data(**kwargs)

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

        if self.request.user.is_authenticated:
            if self.user:
                # Add FlareAid OnetoOne related model objects from the MedicalProfile for the User
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
                    context["heartattack_form"] = self.heartattack_form_class(
                        instance=self.medicalprofile.heartattack
                    )
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
        """Ovewrites get_form_kwargs() to look for 'ultaid' kwarg in GET request, uses 'ultaid' to query database for associated ULTAid for use in PPxAidForm
        returns: [dict: dict containing 'ultaid' kwarg for form]"""
        # Assign self.ultaid from GET request kwargs before calling super() which will overwrite kwargs
        self.ultaid = self.kwargs.get("ultaid", None)
        self.no_user = True
        if self.kwargs.get("username"):
            self.no_user = False
        kwargs = super(PPxAidCreate, self).get_form_kwargs()
        # Checks if flare kwarg came from ULTAid Detail and queries database for ultaid_pk that matches self.ultaid from initial kwargs
        if self.ultaid:
            ultaid = None
            if isinstance(self.ultaid, int):
                ultaid = ULTAid.objects.get(pk=self.ultaid)
            elif isinstance(self.ultaid, str):
                ultaid = ULTAid.objects.get(slug=self.ultaid)
            kwargs["ultaid"] = ultaid
            kwargs["no_user"] = self.no_user
            # If User is anonymous / not logged in and PPxAid has a ULTAid, pass ckd stroke and heartattack from ULTAid to PPxAid to avoid duplication of user input
            if self.no_user == True:
                kwargs["ckd"] = ultaid.ckd
                kwargs["stroke"] = ultaid.stroke
                kwargs["heartattack"] = ultaid.heartattack
        return kwargs

    def get_success_url(self):
        self.ultaid = self.kwargs.get("ultaid", None)
        self.username = self.kwargs.get("username", None)
        if self.ultaid:
            if self.username:
                return reverse("ultaid:user-detail", kwargs={"slug": self.kwargs["ultaid"]})
            else:
                if isinstance(self.ultaid, int):
                    return reverse("ultaid:detail", kwargs={"pk": self.kwargs["ultaid"]})
                else:
                    return reverse("ultaid:detail", kwargs={"slug": self.kwargs["ultaid"]})
        else:
            if self.username:
                return reverse("ppxaid:detail", kwargs={"slug": self.object.slug})
            else:
                return reverse("ppxaid:detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=PPxAid())
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

        ppxaid_data = form.save(commit=False)
        if request.user.is_authenticated:
            if self.medicalprofile:
                anticoagulation_form = self.anticoagulation_form_class(
                    request.POST, instance=self.medicalprofile.anticoagulation
                )
                bleed_form = self.bleed_form_class(request.POST, instance=self.medicalprofile.bleed)
                CKD_form = self.CKD_form_class(request.POST, instance=self.medicalprofile.CKD)
                colchicine_interactions_form = self.colchicine_interactions_form_class(
                    request.POST, instance=self.medicalprofile.colchicine_interactions
                )
                diabetes_form = self.diabetes_form_class(request.POST, instance=self.medicalprofile.diabetes)
                heartattack_form = self.heartattack_form_class(
                    request.POST, instance=self.medicalprofile.heartattack
                )
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
            anticoagulation_data.last_modified = "PPxAid"
            anticoagulation_data.save()
            bleed_data = bleed_form.save(commit=False)
            bleed_data.last_modified = "PPxAid"
            bleed_data.save()
            ckd_data = CKD_form.save(commit=False)
            ckd_data.last_modified = "PPxAid"
            ckd_data.save()
            colchicine_interactions_data = colchicine_interactions_form.save(commit=False)
            colchicine_interactions_data.last_modified = "PPxAid"
            colchicine_interactions_data.save()
            diabetes_data = diabetes_form.save(commit=False)
            diabetes_data.last_modified = "PPxAid"
            diabetes_data.save()
            heartattack_data = heartattack_form.save(commit=False)
            heartattack_data.last_modified = "PPxAid"
            heartattack_data.save()
            IBD_data = IBD_form.save(commit=False)
            IBD_data.last_modified = "PPxAid"
            IBD_data.save()
            osteoporosis_data = osteoporosis_form.save(commit=False)
            osteoporosis_data.last_modified = "PPxAid"
            osteoporosis_data.save()
            stroke_data = stroke_form.save(commit=False)
            stroke_data.last_modified = "PPxAid"
            stroke_data.save()
            ppxaid_data.anticoagulation = anticoagulation_data
            ppxaid_data.bleed = bleed_data
            ppxaid_data.ckd = ckd_data
            ppxaid_data.colchicine_interactions = colchicine_interactions_data
            ppxaid_data.diabetes = diabetes_data
            ppxaid_data.heartattack = heartattack_data
            ppxaid_data.ibd = IBD_data
            ppxaid_data.osteoporosis = osteoporosis_data
            ppxaid_data.stroke = stroke_data
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
                            diabetes_form=self.diabetes_form_class(
                                request.POST, instance=self.medicalprofile.diabetes
                            ),
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


class PPxAidDetail(PatientProviderMixin, DetailView):
    model = PPxAid
    template_name = "ppxaid/ppxaid_detail.html"


class PPxAidUpdate(LoginRequiredMixin, PatientProviderMixin, ProfileMixin, UserMixin, UpdateView):
    model = PPxAid
    form_class = PPxAidForm
    anticoagulation_form_class = AnticoagulationSimpleForm
    bleed_form_class = BleedSimpleForm
    CKD_form_class = CKDForm
    colchicine_interactions_form_class = ColchicineInteractionsSimpleForm
    diabetes_form_class = DiabetesSimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    IBD_form_class = IBDSimpleForm
    osteoporosis_form_class = OsteoporosisSimpleForm
    stroke_form_class = StrokeSimpleForm

    def get_context_data(self, **kwargs):
        context = super(PPxAidUpdate, self).get_context_data(**kwargs)
        # Add PPxAid OnetoOne related model objects from the MedicalProfile for the logged in User
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
                context["CKD_form"] = self.CKD_form_class(self.request.POST, instance=self.object.CKD)
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
                context["IBD_form"] = self.IBD_form_class(self.request.POST, instance=self.object.IBD)
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
                context["heartattack_form"] = self.heartattack_form_class(instance=self.object.heartattack)
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(instance=self.object.IBD)
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(
                    instance=self.object.osteoporosis
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.object.stroke)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Uses UpdateView to get the PPxAid instance requested and put it in a form
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
        heartattack_form = self.heartattack_form_class(
            request.POST, instance=self.object.heartattack
        )
        IBD_form = self.IBD_form_class(request.POST, instance=self.object.IBD)
        osteoporosis_form = self.osteoporosis_form_class(
            request.POST, instance=self.object.osteoporosis
        )
        stroke_form = self.stroke_form_class(request.POST, instance=self.object.stroke)

        if form.is_valid():
            ppxaid_data = form.save(commit=False)
            if anticoagulation_form.is_valid():
                #if "value" in anticoagulation_form.changed_data:
                anticoagulation_data = anticoagulation_form.save(commit=False)
                anticoagulation_data.last_modified = "FlareAid"
                anticoagulation_data.save()
                ppxaid_data.anticoagulation = anticoagulation_data
            if bleed_form.is_valid():
                #if "value" in bleed_form.changed_data:
                bleed_data = bleed_form.save(commit=False)
                bleed_data.last_modified = "FlareAid"
                bleed_data.save()
                ppxaid_data.bleed = bleed_data
            if CKD_form.is_valid():
                #if "value" in CKD_form.changed_data:
                ckd_data = CKD_form.save(commit=False)
                ckd_data.last_modified = "FlareAid"
                ckd_data.save()
                ppxaid_data.ckd = ckd_data
            if colchicine_interactions_form.is_valid():
                #if "value" in colchicine_interactions_form.changed_data:
                colchicine_interactions_data = colchicine_interactions_form.save(commit=False)
                colchicine_interactions_data.last_modified = "FlareAid"
                colchicine_interactions_data.save()
                ppxaid_data.colchicine_interactions = colchicine_interactions_data
            if diabetes_form.is_valid():
                #if "value" in diabetes_form.changed_data:
                diabetes_data = diabetes_form.save(commit=False)
                diabetes_data.last_modified = "FlareAid"
                diabetes_data.save()
                ppxaid_data.diabetes = diabetes_data
            if heartattack_form.is_valid():
                #if "value" in heartattack_form.changed_data:
                heartattack_data = heartattack_form.save(commit=False)
                heartattack_data.last_modified = "FlareAid"
                heartattack_data.save()
                ppxaid_data.heartattack = heartattack_data
            if IBD_form.is_valid():
                #if "value" in IBD_form.changed_data:
                IBD_data = IBD_form.save(commit=False)
                IBD_data.last_modified = "FlareAid"
                IBD_data.save()
                ppxaid_data.ibd = IBD_data
            if osteoporosis_form.is_valid():
                #if "value" in osteoporosis_form.changed_data:
                osteoporosis_data = osteoporosis_form.save(commit=False)
                osteoporosis_data.last_modified = "FlareAid"
                osteoporosis_data.save()
                ppxaid_data.osteoporosis = osteoporosis_data
            if stroke_form.is_valid():
                #if "value" in stroke_form.changed_data:
                stroke_data = stroke_form.save(commit=False)
                stroke_data.last_modified = "FlareAid"
                stroke_data.save()
                ppxaid_data.stroke = stroke_data
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
                    diabetes_form=self.diabetes_form_class(
                        request.POST, instance=self.object.diabetes
                    ),
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
