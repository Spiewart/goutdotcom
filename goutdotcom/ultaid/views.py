from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from ..history.forms import (
    AllopurinolHypersensitivitySimpleForm,
    CKDForm,
    ErosionsForm,
    FebuxostatHypersensitivitySimpleForm,
    HeartAttackSimpleForm,
    OrganTransplantForm,
    StrokeSimpleForm,
    TophiForm,
    XOIInteractionsSimpleForm,
)
from ..history.models import (
    CKD,
    AllopurinolHypersensitivity,
    Erosions,
    FebuxostatHypersensitivity,
    HeartAttack,
    OrganTransplant,
    Stroke,
    Tophi,
    XOIInteractions,
)
from ..ppxaid.models import PPxAid
from ..ult.models import ULT
from ..utils.mixins import (
    PatientProviderCreateMixin,
    PatientProviderMixin,
    ProfileMixin,
    UserMixin,
)
from .forms import ULTAidForm
from .mixins import ULTMixin
from .models import ULTAid

User = get_user_model()


class ULTAidCreate(PatientProviderCreateMixin, ProfileMixin, SuccessMessageMixin, ULTMixin, UserMixin, CreateView):
    model = ULTAid
    form_class = ULTAidForm
    CKD_form_class = CKDForm
    erosions_form_class = ErosionsForm
    XOI_interactions_form_class = XOIInteractionsSimpleForm
    organ_transplant_form_class = OrganTransplantForm
    allopurinol_hypersensitivity_form_class = AllopurinolHypersensitivitySimpleForm
    febuxostat_hypersensitivity_form_class = FebuxostatHypersensitivitySimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    stroke_form_class = StrokeSimpleForm
    tophi_form_class = TophiForm

    success_message = "ULTAid successfully created!"

    def form_valid(self, form):
        # Check if POST has 'ult' kwarg and assign ULTAid ult OnetoOne related object based on pk='ult'
        if self.ult:
            form.instance.erosions = self.ult.erosions
            form.instance.tophi = self.ult.tophi
            # Check if ULT calculator() result was indicated or conditional and set ULTAid need field true if so, False if not
            if self.ult.calculator() == "Indicated" or self.ult.calculator() == "Conditional":
                form.instance.need = True
            else:
                form.instance.need = False
            # If user is not authenticated and created a ULTAid from a ULT, use ULT CKD instance instead of making new one, removed forms in form via Kwargs and layout objects
            if self.request.user.is_authenticated == False:
                if form.instance.ult.ckd.value == False:
                    form.instance.ckd = form.instance.ult.ckd
        if self.request.user.is_authenticated:
            form.instance.creator = self.request.user
        if self.user:
            form.instance.user = self.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Checks if user is logged in, if they have already created a ULTAid, and redirects to UpdateView if so
        if self.request.user.is_authenticated:
            if self.user:
                try:
                    self.ultaid = ULTAid.objects.get(slug=self.user.username)
                except ObjectDoesNotExist:
                    self.ultaid = None
                if self.ultaid:
                    return redirect("ultaid:update", slug=self.ultaid.slug)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ULTAidCreate, self).get_context_data(**kwargs)

        def get_blank_forms():
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(self.request.GET)
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(self.request.GET)
            if "XOI_interactions_form" not in context:
                context["XOI_interactions_form"] = self.XOI_interactions_form_class(self.request.GET)
            if "organ_transplant_form" not in context:
                context["organ_transplant_form"] = self.organ_transplant_form_class(self.request.GET)
            if "allopurinol_hypersensitivity_form" not in context:
                context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                    self.request.GET
                )
            if "febuxostat_hypersensitivity_form" not in context:
                context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                    self.request.GET
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(self.request.GET)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(self.request.GET)
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(self.request.GET)

        if self.request.user.is_authenticated:
            if self.user:
                # Check if User has ULT, pass to ULTAid view/context for JQuery evaluation to update form fields
                try:
                    self.user_ult = self.user.ult
                except:
                    self.user_ult = None
                if self.user_ult:
                    context["user_ult"] = self.user.ult.calculator()
                # Fetch related model instances via User object
                if "CKD_form" not in context:
                    context["CKD_form"] = self.CKD_form_class(instance=self.medicalprofile.CKD)
                if "erosions_form" not in context:
                    context["erosions_form"] = self.erosions_form_class(instance=self.medicalprofile.erosions)
                if "XOI_interactions_form" not in context:
                    context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                        instance=self.medicalprofile.XOI_interactions
                    )
                if "organ_transplant_form" not in context:
                    context["organ_transplant_form"] = self.organ_transplant_form_class(
                        instance=self.medicalprofile.organ_transplant
                    )
                if "allopurinol_hypersensitivity_form" not in context:
                    context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                        instance=self.medicalprofile.allopurinol_hypersensitivity
                    )
                if "febuxostat_hypersensitivity_form" not in context:
                    context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                        instance=self.medicalprofile.febuxostat_hypersensitivity
                    )
                if "heartattack_form" not in context:
                    context["heartattack_form"] = self.heartattack_form_class(instance=self.medicalprofile.heartattack)
                if "stroke_form" not in context:
                    context["stroke_form"] = self.stroke_form_class(instance=self.medicalprofile.stroke)
                if "tophi_form" not in context:
                    context["tophi_form"] = self.tophi_form_class(instance=self.medicalprofile.tophi)
            else:
                get_blank_forms()
        else:
            get_blank_forms()
        return context

    def get_form_kwargs(self, **kwargs):
        """Ovewrites get_form_kwargs() to look for 'ult' kwarg in GET request
        Uses 'ult' to query database for associated ULT for use in ULTAidForm
        returns: [dict: dict containing 'ult' kwarg for form]"""
        # Assign self.flare from GET request kwargs before calling super() which will overwrite kwargs
        self.no_user = False
        if self.request.user.is_authenticated == False:
            self.no_user = True
        kwargs = super(ULTAidCreate, self).get_form_kwargs()
        # Check if ult kwarg came from ULTDetail view or otherwise
        if self.ult:
            kwargs["ult"] = self.ult
            kwargs["no_user"] = self.no_user
            # If User is anonymous / not logged in and FlareAid has a Flare, pass ckd from ULT to ULTAid to avoid duplication of user input
            if self.request.user.is_authenticated == False:
                kwargs["ckd"] = self.ult.ckd
        return kwargs

    # This unfortunately needs to get rewritten and the object assigned at the start of POST once you mess with enough CBV code. Not sure what exactly triggers it.
    def get_object(self):
        object = self.model
        return object

    def get_success_url(self):
        # Check if there is a slug kwarg and redirect to DetailView using that
        if self.user:
            return reverse("ultaid:user-detail", kwargs={"slug": self.object.slug})
        # Otherwise return to DetailView based on PK
        else:
            return reverse(
                "ultaid:detail",
                kwargs={
                    "pk": self.object.pk,
                },
            )

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, instance=ULTAid())
        self.object = self.get_object()
        CKD_form = self.CKD_form_class(request.POST, instance=CKD())
        erosions_form = self.erosions_form_class(request.POST, instance=Erosions())
        XOI_interactions_form = self.XOI_interactions_form_class(request.POST, instance=XOIInteractions())
        organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=OrganTransplant())
        allopurinol_hypersensitivity_form = self.allopurinol_hypersensitivity_form_class(
            request.POST, instance=AllopurinolHypersensitivity()
        )
        febuxostat_hypersensitivity_form = self.febuxostat_hypersensitivity_form_class(
            request.POST, instance=FebuxostatHypersensitivity()
        )
        heartattack_form = self.heartattack_form_class(request.POST, instance=HeartAttack())
        stroke_form = self.stroke_form_class(request.POST, instance=Stroke())
        tophi_form = self.tophi_form_class(request.POST, instance=Tophi())

        if form.is_valid():
            ULTAid_data = form.save(commit=False)
            # Set PPxaid to None to declare in scope
            self.ppxaid = None
            # Check if user is authenticated and pull OnetoOne related model data from MedicalProfile if so
            if request.user.is_authenticated:
                if self.medicalprofile:
                    # See if User has PPxAid
                    try:
                        self.ppxaid = self.user.ppxaid
                    except PPxAid.DoesNotExist:
                        self.ppxaid = None
                    # Assign User to ULTAid form to avoid repeating the query in form_valid()
                    CKD_form = self.CKD_form_class(request.POST, instance=self.medicalprofile.CKD)
                    erosions_form = self.erosions_form_class(request.POST, instance=self.medicalprofile.erosions)
                    XOI_interactions_form = self.XOI_interactions_form_class(
                        request.POST, instance=self.medicalprofile.XOI_interactions
                    )
                    organ_transplant_form = self.organ_transplant_form_class(
                        request.POST, instance=self.medicalprofile.organ_transplant
                    )
                    allopurinol_hypersensitivity_form = self.allopurinol_hypersensitivity_form_class(
                        request.POST, instance=self.medicalprofile.allopurinol_hypersensitivity
                    )
                    febuxostat_hypersensitivity_form = self.febuxostat_hypersensitivity_form_class(
                        request.POST, instance=self.medicalprofile.febuxostat_hypersensitivity
                    )
                    heartattack_form = self.heartattack_form_class(
                        request.POST, instance=self.medicalprofile.heartattack
                    )
                    stroke_form = self.stroke_form_class(request.POST, instance=self.medicalprofile.stroke)
                    tophi_form = self.tophi_form_class(request.POST, instance=self.medicalprofile.tophi)
            if CKD_form.is_valid():
                CKD_data = CKD_form.save(commit=False)
                CKD_data.last_modified = "ULTAid"
                CKD_data.save()
            if erosions_form.is_valid():
                erosions_data = erosions_form.save(commit=False)
                erosions_data.last_modified = "ULTAid"
                erosions_data.save()
            if XOI_interactions_form.is_valid():
                XOI_interactions_data = XOI_interactions_form.save(commit=False)
                XOI_interactions_data.last_modified = "ULTAid"
                XOI_interactions_data.save()
            if organ_transplant_form.is_valid():
                organ_transplant_data = organ_transplant_form.save(commit=False)
                organ_transplant_data.last_modified = "ULTAid"
                organ_transplant_data.save()
            if allopurinol_hypersensitivity_form.is_valid():
                allopurinol_hypersensitivity_data = allopurinol_hypersensitivity_form.save(commit=False)
                allopurinol_hypersensitivity_data.last_modified = "ULTAid"
                allopurinol_hypersensitivity_data.save()
            if febuxostat_hypersensitivity_form.is_valid():
                febuxostat_hypersensitivity_data = febuxostat_hypersensitivity_form.save(commit=False)
                febuxostat_hypersensitivity_data.last_modified = "ULTAid"
                febuxostat_hypersensitivity_data.save()
            if heartattack_form.is_valid():
                heartattack_data = heartattack_form.save(commit=False)
                heartattack_data.last_modified = "ULTAid"
                heartattack_data.save()
            if stroke_form.is_valid():
                stroke_data = stroke_form.save(commit=False)
                stroke_data.last_modified = "ULTAid"
                stroke_data.save()
            if tophi_form.is_valid():
                tophi_data = tophi_form.save(commit=False)
                tophi_data.last_modified = "ULTAid"
                tophi_data.save()
            ULTAid_data.ckd = CKD_data
            ULTAid_data.erosions = erosions_data
            ULTAid_data.XOI_interactions = XOI_interactions_data
            ULTAid_data.organ_transplant = organ_transplant_data
            ULTAid_data.allopurinol_hypersensitivity = allopurinol_hypersensitivity_data
            ULTAid_data.febuxostat_hypersensitivity = febuxostat_hypersensitivity_data
            ULTAid_data.heartattack = heartattack_data
            ULTAid_data.stroke = stroke_data
            ULTAid_data.tophi = tophi_data
            ULTAid_data.save()
            # Check if User has already created a PPxAid for some reason
            # If so, assign it to the newly created/saved ULTAid to that attribute on the PPxAid
            if self.ppxaid:
                self.ppxaid.ultaid = ULTAid_data
                self.ppxaid.save()
            return self.form_valid(form)
        else:
            if request.user.is_authenticated:
                # If User is logged in, see if there is username kwarg
                if self.medicalprofile:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            CKD_form=self.CKD_form_class(request.POST, instance=self.medicalprofile.CKD),
                            erosions_form=self.erosions_form_class(request.POST, instance=self.medicalprofile.erosions),
                            XOI_interactions_form=self.XOI_interactions_form_class(
                                request.POST, instance=self.medicalprofile.XOI_interactions
                            ),
                            organ_transplant_form=self.organ_transplant_form_class(
                                request.POST, instance=self.medicalprofile.organ_transplant
                            ),
                            allopurinol_hypersensitivity_form=self.allopurinol_hypersensitivity_form_class(
                                request.POST, instance=self.medicalprofile.allopurinol_hypersensitivity
                            ),
                            febuxostat_hypersensitivity_form=self.febuxostat_hypersensitivity_form_class(
                                request.POST, instance=self.medicalprofile.febuxostat_hypersensitivity
                            ),
                            heartattack_form=self.heartattack_form_class(
                                request.POST, instance=self.medicalprofile.heartattack
                            ),
                            stroke_form=self.stroke_form_class(request.POST, instance=self.medicalprofile.stroke),
                            tophi_form=self.tophi_form_class(request.POST, instance=self.medicalprofile.tophi),
                        )
                    )
                else:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            CKD_form=self.CKD_form_class(request.POST, instance=CKD()),
                            erosions_form=self.erosions_form_class(request.POST, instance=Erosions()),
                            XOI_interactions_form=self.XOI_interactions_form_class(
                                request.POST, instance=XOIInteractions()
                            ),
                            organ_transplant_form=self.organ_transplant_form_class(
                                request.POST, instance=OrganTransplant()
                            ),
                            allopurinol_hypersensitivity_form=self.allopurinol_hypersensitivity_form_class(
                                request.POST, instance=AllopurinolHypersensitivity()
                            ),
                            febuxostat_hypersensitivity_form=self.febuxostat_hypersensitivity_form_class(
                                request.POST, instance=FebuxostatHypersensitivity()
                            ),
                            heartattack_form=self.heartattack_form_class(request.POST, instance=HeartAttack()),
                            stroke_form=self.stroke_form_class(request.POST, instance=Stroke()),
                            tophi_form=self.tophi_form_class(request.POST, instance=Tophi()),
                        )
                    )
            else:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        CKD_form=self.CKD_form_class(request.POST, instance=CKD()),
                        erosions_form=self.erosions_form_class(request.POST, instance=Erosions()),
                        XOI_interactions_form=self.XOI_interactions_form_class(
                            request.POST, instance=XOIInteractions()
                        ),
                        organ_transplant_form=self.organ_transplant_form_class(
                            request.POST, instance=OrganTransplant()
                        ),
                        allopurinol_hypersensitivity_form=self.allopurinol_hypersensitivity_form_class(
                            request.POST, instance=AllopurinolHypersensitivity()
                        ),
                        febuxostat_hypersensitivity_form=self.febuxostat_hypersensitivity_form_class(
                            request.POST, instance=FebuxostatHypersensitivity()
                        ),
                        heartattack_form=self.heartattack_form_class(request.POST, instance=HeartAttack()),
                        stroke_form=self.stroke_form_class(request.POST, instance=Stroke()),
                        tophi_form=self.tophi_form_class(request.POST, instance=Tophi()),
                    )
                )


class ULTAidDetail(PatientProviderMixin, DetailView):
    model = ULTAid


class ULTAidUpdate(LoginRequiredMixin, PatientProviderMixin, SuccessMessageMixin, ULTMixin, UpdateView):
    model = ULTAid
    form_class = ULTAidForm
    CKD_form_class = CKDForm
    erosions_form_class = ErosionsForm
    XOI_interactions_form_class = XOIInteractionsSimpleForm
    organ_transplant_form_class = OrganTransplantForm
    allopurinol_hypersensitivity_form_class = AllopurinolHypersensitivitySimpleForm
    febuxostat_hypersensitivity_form_class = FebuxostatHypersensitivitySimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    stroke_form_class = StrokeSimpleForm
    tophi_form_class = TophiForm

    success_message = "ULTAid successfully updated!"

    def get_context_data(self, **kwargs):
        context = super(ULTAidUpdate, self).get_context_data(**kwargs)
        # Check if User has ULT, pass to ULTAid view/context for JQuery evaluation to update form fields
        if self.ult:
            context["user_ult"] = ULT.objects.get(user=self.user).calculator()
        # Adds appropriate OnetoOne related History/MedicalProfile model forms to context
        if self.request.POST:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(self.request.POST, instance=self.object.ckd)
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(self.request.POST, instance=self.object.erosions)
            if "XOI_interactions_form" not in context:
                context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                    self.request.POST, instance=self.object.XOI_interactions
                )
            if "organ_transplant_form" not in context:
                context["organ_transplant_form"] = self.organ_transplant_form_class(
                    self.request.POST, instance=self.object.organ_transplant
                )
            if "allopurinol_hypersensitivity_form" not in context:
                context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                    self.request.POST, instance=self.object.allopurinol_hypersensitivity
                )
            if "febuxostat_hypersensitivity_form" not in context:
                context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                    self.request.POST, instance=self.object.febuxostat_hypersensitivity
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    self.request.POST, instance=self.object.heartattack
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(self.request.POST, instance=self.object.stroke)
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(self.request.POST, instance=self.object.tophi)
        else:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.object.ckd)
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(instance=self.object.erosions)
            if "XOI_interactions_form" not in context:
                context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                    instance=self.object.XOI_interactions
                )
            if "organ_transplant_form" not in context:
                context["organ_transplant_form"] = self.organ_transplant_form_class(
                    instance=self.object.organ_transplant
                )
            if "allopurinol_hypersensitivity_form" not in context:
                context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                    instance=self.object.allopurinol_hypersensitivity
                )
            if "febuxostat_hypersensitivity_form" not in context:
                context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                    instance=self.object.febuxostat_hypersensitivity
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(instance=self.object.heartattack)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.object.stroke)
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(instance=self.object.tophi)
        return context

    def get_success_url(self):
        # Check if there is a slug (username) kwarg and redirect to DetailView using that
        if self.kwargs.get("slug"):
            return reverse("ultaid:user-detail", kwargs={"slug": self.kwargs["slug"]})
        # Otherwise return to DetailView based on PK
        else:
            return reverse(
                "ultaid:detail",
                kwargs={
                    "pk": self.object.pk,
                },
            )

    def post(self, request, **kwargs):
        # Uses UpdateView to get the ULTAid instance requested and put it in a form
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        # Fetch related models to instantiate related model forms
        CKD_form = self.CKD_form_class(request.POST, instance=self.object.ckd)
        erosions_form = self.erosions_form_class(request.POST, instance=self.object.erosions)
        XOI_interactions_form = self.XOI_interactions_form_class(request.POST, instance=self.object.XOI_interactions)
        organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=self.object.organ_transplant)
        allopurinol_hypersensitivity_form = self.allopurinol_hypersensitivity_form_class(
            request.POST, instance=self.object.allopurinol_hypersensitivity
        )
        febuxostat_hypersensitivity_form = self.febuxostat_hypersensitivity_form_class(
            request.POST, instance=self.object.febuxostat_hypersensitivity
        )
        heartattack_form = self.heartattack_form_class(request.POST, instance=self.object.heartattack)
        stroke_form = self.stroke_form_class(request.POST, instance=self.object.stroke)
        tophi_form = self.tophi_form_class(request.POST, instance=self.object.tophi)

        if form.is_valid():
            # Uses related OnetoOne field forms to populate ULTAid fields, changes last_modified to ULTAid, and saves all data
            ULTAid_data = form.save(commit=False)
            if CKD_form.is_valid():
                CKD_data = CKD_form.save(commit=False)
                if "value" in CKD_form.changed_data:
                    CKD_data.last_modified = "ULTAid"
                CKD_data.save()
                ULTAid_data.ckd = CKD_data
            if erosions_form.is_valid():
                erosions_data = erosions_form.save(commit=False)
                if "value" in erosions_form.changed_data:
                    erosions_data.last_modified = "ULTAid"
                erosions_data.save()
                ULTAid_data.erosions = erosions_data
            if XOI_interactions_form.is_valid():
                XOI_interactions_data = XOI_interactions_form.save(commit=False)
                if "value" in XOI_interactions_form.changed_data:
                    XOI_interactions_data.last_modified = "ULTAid"
                XOI_interactions_data.save()
                ULTAid_data.XOI_interactions = XOI_interactions_data
            if organ_transplant_form.is_valid():
                organ_transplant_data = organ_transplant_form.save(commit=False)
                if "value" in organ_transplant_form.changed_data:
                    organ_transplant_data.last_modified = "ULTAid"
                organ_transplant_data.save()
                ULTAid_data.organ_transplant = organ_transplant_data
            if allopurinol_hypersensitivity_form.is_valid():
                allopurinol_hypersensitivity_data = allopurinol_hypersensitivity_form.save(commit=False)
                if "value" in allopurinol_hypersensitivity_form.changed_data:
                    allopurinol_hypersensitivity_data.last_modified = "ULTAid"
                allopurinol_hypersensitivity_data.save()
                ULTAid_data.allopurinol_hypersensitivity = allopurinol_hypersensitivity_data
            if febuxostat_hypersensitivity_form.is_valid():
                febuxostat_hypersensitivity_data = febuxostat_hypersensitivity_form.save(commit=False)
                if "value" in febuxostat_hypersensitivity_form.changed_data:
                    febuxostat_hypersensitivity_data.last_modified = "ULTAid"
                febuxostat_hypersensitivity_data.save()
                ULTAid_data.febuxostat_hypersensitivity = febuxostat_hypersensitivity_data
            if heartattack_form.is_valid():
                heartattack_data = heartattack_form.save(commit=False)
                if "value" in heartattack_form.changed_data:
                    heartattack_data.last_modified = "ULTAid"
                heartattack_data.save()
                ULTAid_data.heartattack = heartattack_data
            if stroke_form.is_valid():
                stroke_data = stroke_form.save(commit=False)
                if "value" in stroke_form.changed_data:
                    stroke_data.last_modified = "ULTAid"
                stroke_data.save()
                ULTAid_data.stroke = stroke_data
            if tophi_form.is_valid():
                tophi_data = tophi_form.save(commit=False)
                if "value" in tophi_form.changed_data:
                    tophi_data.save()
                ULTAid_data.tophi = tophi_data
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    CKD_form=self.CKD_form_class(request.POST, instance=self.object.ckd),
                    erosions_form=self.erosions_form_class(request.POST, instance=self.object.erosions),
                    XOI_interactions_form=self.XOI_interactions_form_class(
                        request.POST, instance=self.object.XOI_interactions
                    ),
                    organ_transplant_form=self.organ_transplant_form_class(
                        request.POST, instance=self.object.organ_transplant
                    ),
                    allopurinol_hypersensitivity_form=self.allopurinol_hypersensitivity_form_class(
                        request.POST, instance=self.object.allopurinol_hypersensitivity
                    ),
                    febuxostat_hypersensitivity_form=self.febuxostat_hypersensitivity_form_class(
                        request.POST, instance=self.object.febuxostat_hypersensitivity
                    ),
                    heartattack_form=self.heartattack_form_class(request.POST, instance=self.object.heartattack),
                    stroke_form=self.stroke_form_class(request.POST, instance=self.object.stroke),
                    tophi_form=self.tophi_form_class(request.POST, instance=self.object.tophi),
                )
            )
