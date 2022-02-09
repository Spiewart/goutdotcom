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
from ..utils.mixins import PatientProviderCreateMixin, PatientProviderMixin
from .forms import ULTAidForm
from .models import ULTAid

User = get_user_model()


class ULTAidCreate(PatientProviderCreateMixin, SuccessMessageMixin, CreateView):
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
        if self.kwargs.get("ult"):
            self.ult = self.kwargs.get("ult")
            form.instance.ult = None
            if isinstance(self.ult, int):
                form.instance.ult = ULT.objects.get(pk=self.kwargs.get("ult"))
            else:
                form.instance.ult = ULT.objects.get(slug=self.kwargs.get("ult"))
            form.instance.erosions = form.instance.ult.erosions
            form.instance.tophi = form.instance.ult.tophi
            # Check if ULT calculator() result was indicated or conditional and set ULTAid need field true if so, False if not
            if form.instance.ult.calculator() == "Indicated" or form.instance.ult.calculator() == "Conditional":
                form.instance.need = True
            else:
                form.instance.need = False
            # If user is not authenticated and created a ULTAid from a ULT, use ULT CKD instance instead of making new one, removed forms in form via Kwargs and layout objects
            if self.request.user.is_authenticated == False:
                if form.instance.ult.ckd.value == False:
                    form.instance.ckd = form.instance.ult.ckd
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Checks if user is logged in, if they have already created a ULTAid, and redirects to UpdateView if so
        if self.request.user.is_authenticated:
            if self.kwargs.get("username"):
                self.username = self.kwargs.get("username")
                try:
                    self.ultaid = ULTAid.objects.get(slug=self.username)
                except ObjectDoesNotExist:
                    self.ultaid = None
                if self.ultaid:
                    return redirect("ultaid:update", slug=self.ultaid.slug)
                else:
                    super().get(request, *args, **kwargs)
            else:
                super().get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ULTAidCreate, self).get_context_data(**kwargs)
        # Add ULTAid OnetoOne related model objects from the MedicalProfile for the logged in User
        try:
            self.ult = self.kwargs.get("ult")
        except:
            self.ult = None
        if self.ult:
            if isinstance(self.ult, int):
                context["ult"] = ULT.objects.get(pk=self.ult)
            else:
                context["ult"] = ULT.objects.get(slug=self.ult)
        if self.request.user.is_authenticated:
            # If User is logged in, see if there is username kwarg
            try:
                self.username = self.kwargs.get("username")
            except:
                self.username = None
            # If there is a username, fetch associated User and related MedicalProfile objects
            # Add forms with User's related model instances
            if self.username:
                self.user = User.objects.get(username=self.username)
                try:
                    self.ult = self.user.ult
                except:
                    self.ult = None
                if self.ult:
                    context["user_ult"] = ULT.objects.get(user=self.user).calculator()
                # Fetch related model instances via User object
                if "CKD_form" not in context:
                    context["CKD_form"] = self.CKD_form_class(instance=self.user.medicalprofile.CKD)
                if "erosions_form" not in context:
                    context["erosions_form"] = self.erosions_form_class(instance=self.user.medicalprofile.erosions)
                if "XOI_interactions_form" not in context:
                    context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                        instance=self.user.medicalprofile.XOI_interactions
                    )
                if "organ_transplant_form" not in context:
                    context["organ_transplant_form"] = self.organ_transplant_form_class(
                        instance=self.user.medicalprofile.organ_transplant
                    )
                if "allopurinol_hypersensitivity_form" not in context:
                    context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                        instance=self.user.medicalprofile.allopurinol_hypersensitivity
                    )
                if "febuxostat_hypersensitivity_form" not in context:
                    context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                        instance=self.user.medicalprofile.febuxostat_hypersensitivity
                    )
                if "heartattack_form" not in context:
                    context["heartattack_form"] = self.heartattack_form_class(
                        instance=self.user.medicalprofile.heartattack
                    )
                if "stroke_form" not in context:
                    context["stroke_form"] = self.stroke_form_class(instance=self.user.medicalprofile.stroke)
                if "tophi_form" not in context:
                    context["tophi_form"] = self.tophi_form_class(instance=self.user.medicalprofile.tophi)
            else:
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
        else:
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
        return context

    def get_form_kwargs(self):
        """Ovewrites get_form_kwargs() to look for 'ult' kwarg in GET request
        Uses 'ult' to query database for associated ULT for use in ULTAidForm
        returns: [dict: dict containing 'ult' kwarg for form]"""
        # Assign self.flare from GET request kwargs before calling super() which will overwrite kwargs
        self.ult = self.kwargs.get("ult", None)
        self.no_user = False
        if self.request.user.is_authenticated == False:
            self.no_user = True
        kwargs = super(ULTAidCreate, self).get_form_kwargs()
        # Check if ult kwarg came from ULTDetail view or otherwise
        if self.ult:
            # Check if ULT is a pk or a slug
            # Fetch ULT based on pk or slug
            if isinstance(self.ult, int):
                ult_pk = self.ult
                ult = ULT.objects.get(pk=ult_pk)
            elif isinstance(self.ult, str):
                ult_slug = self.ult
                ult = ULT.objects.get(slug=ult_slug)
            kwargs["ult"] = ult
            kwargs["no_user"] = self.no_user
            # If User is anonymous / not logged in and FlareAid has a Flare, pass ckd from ULT to ULTAid to avoid duplication of user input
            if self.request.user.is_authenticated == False:
                kwargs["ckd"] = ult.ckd
        return kwargs

    # This unfortunately needs to get rewritten and the object assigned at the start of POST once you mess with enough CBV code. Not sure what exactly triggers it.
    def get_object(self):
        object = self.model
        return object

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
            # Set User and PPxaid to None to declare in scope
            self.user = None
            self.ppxaid = None
            # Check if user is authenticated and pull OnetoOne related model data from MedicalProfile if so
            if request.user.is_authenticated:
                # If User is logged in, see if there is username kwarg
                try:
                    self.username = self.kwargs.get("username")
                except:
                    self.username = None
                # If there is a username, fetch associated User and related MedicalProfile objects
                # Overwrite forms defined above with User instances
                if self.username:
                    self.user = User.objects.get(username=self.username)
                    ULTAid_data.user = self.user
                    # See if User has PPxAid
                    try:
                        self.ppxaid = self.user.ppxaid
                    except PPxAid.DoesNotExist:
                        self.ppxaid = None
                    # Assign User to ULTAid form to avoid repeating the query in form_valid()
                    CKD_form = self.CKD_form_class(request.POST, instance=self.user.medicalprofile.CKD)
                    erosions_form = self.erosions_form_class(request.POST, instance=self.user.medicalprofile.erosions)
                    XOI_interactions_form = self.XOI_interactions_form_class(
                        request.POST, instance=self.user.medicalprofile.XOI_interactions
                    )
                    organ_transplant_form = self.organ_transplant_form_class(
                        request.POST, instance=self.user.medicalprofile.organ_transplant
                    )
                    allopurinol_hypersensitivity_form = self.allopurinol_hypersensitivity_form_class(
                        request.POST, instance=self.user.medicalprofile.allopurinol_hypersensitivity
                    )
                    febuxostat_hypersensitivity_form = self.febuxostat_hypersensitivity_form_class(
                        request.POST, instance=self.user.medicalprofile.febuxostat_hypersensitivity
                    )
                    heartattack_form = self.heartattack_form_class(
                        request.POST, instance=self.user.medicalprofile.heartattack
                    )
                    stroke_form = self.stroke_form_class(request.POST, instance=self.user.medicalprofile.stroke)
                    tophi_form = self.tophi_form_class(request.POST, instance=self.user.medicalprofile.tophi)
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
            # Check if User has already created a PPxAid for some reason and, if so, assign it to the newly created/saved ULTAid to that attribute on the PPxAid
            if self.ppxaid:
                self.ppxaid.ultaid = ULTAid_data
                self.ppxaid.save()
            return self.form_valid(form)
        else:
            if request.user.is_authenticated:
                # If User is logged in, see if there is username kwarg
                try:
                    self.username = self.kwargs.get("username")
                except:
                    self.username = None
                # If there is a username, fetch associated User and related MedicalProfile objects
                # Overwrite forms defined above with User instances
                if self.username:
                    self.user = User.objects.get(username=self.username)
                else:
                    self.user = self.request.user
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        CKD_form=self.CKD_form_class(request.POST, instance=self.user.medicalprofile.CKD),
                        erosions_form=self.erosions_form_class(
                            request.POST, instance=self.user.medicalprofile.erosions
                        ),
                        XOI_interactions_form=self.XOI_interactions_form_class(
                            request.POST, instance=self.user.medicalprofile.XOI_interactions
                        ),
                        organ_transplant_form=self.organ_transplant_form_class(
                            request.POST, instance=self.user.medicalprofile.organ_transplant
                        ),
                        allopurinol_hypersensitivity_form=self.allopurinol_hypersensitivity_form_class(
                            request.POST, instance=self.user.medicalprofile.allopurinol_hypersensitivity
                        ),
                        febuxostat_hypersensitivity_form=self.febuxostat_hypersensitivity_form_class(
                            request.POST, instance=self.user.medicalprofile.febuxostat_hypersensitivity
                        ),
                        heartattack_form=self.heartattack_form_class(
                            request.POST, instance=self.user.medicalprofile.heartattack
                        ),
                        stroke_form=self.stroke_form_class(request.POST, instance=self.user.medicalprofile.stroke),
                        tophi_form=self.tophi_form_class(request.POST, instance=self.user.medicalprofile.tophi),
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


class ULTAidUpdate(LoginRequiredMixin, PatientProviderMixin, SuccessMessageMixin, UpdateView):
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
        # Get User based off object slug in URL
        self.user = User.objects.get(username=self.kwargs.get("slug"))
        # Check if User has ULT, pass to ULTAid view/context for JQuery evaluation to update form fields
        try:
            self.ult = self.user.ult
        except:
            self.ult = None
        if self.ult:
            context["user_ult"] = ULT.objects.get(user=self.user).calculator()
        # Adds appropriate OnetoOne related History/MedicalProfile model forms to context
        if self.request.POST:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(self.request.POST, instance=self.user.medicalprofile.CKD)
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(
                    self.request.POST, instance=self.user.medicalprofile.erosions
                )
            if "XOI_interactions_form" not in context:
                context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                    self.request.POST, instance=self.user.medicalprofile.XOI_interactions
                )
            if "organ_transplant_form" not in context:
                context["organ_transplant_form"] = self.organ_transplant_form_class(
                    self.request.POST, instance=self.user.medicalprofile.organ_transplant
                )
            if "allopurinol_hypersensitivity_form" not in context:
                context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                    self.request.POST, instance=self.user.medicalprofile.allopurinol_hypersensitivity
                )
            if "febuxostat_hypersensitivity_form" not in context:
                context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                    self.request.POST, instance=self.user.medicalprofile.febuxostat_hypersensitivity
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    self.request.POST, instance=self.user.medicalprofile.heartattack
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(
                    self.request.POST, instance=self.user.medicalprofile.stroke
                )
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(
                    self.request.POST, instance=self.user.medicalprofile.tophi
                )
            return context
        else:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.user.medicalprofile.CKD)
            if "erosions_form" not in context:
                context["erosions_form"] = self.erosions_form_class(instance=self.user.medicalprofile.erosions)
            if "XOI_interactions_form" not in context:
                context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                    instance=self.user.medicalprofile.XOI_interactions
                )
            if "organ_transplant_form" not in context:
                context["organ_transplant_form"] = self.organ_transplant_form_class(
                    instance=self.user.medicalprofile.organ_transplant
                )
            if "allopurinol_hypersensitivity_form" not in context:
                context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                    instance=self.user.medicalprofile.allopurinol_hypersensitivity
                )
            if "febuxostat_hypersensitivity_form" not in context:
                context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                    instance=self.user.medicalprofile.febuxostat_hypersensitivity
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(instance=self.user.medicalprofile.heartattack)
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.user.medicalprofile.stroke)
            if "tophi_form" not in context:
                context["tophi_form"] = self.tophi_form_class(instance=self.user.medicalprofile.tophi)
            return context

    def get_success_url(self):
        # Check if there is a slug (username) kwarg and redirect to DetailView using that
        print(self.kwargs.get("slug"))
        if self.kwargs.get("slug"):
            return reverse("ultaid:user-detail", kwargs={"slug": self.kwargs["slug"]})
        # Otherwise return to DetailView based on PK
        else:
            return reverse(
                "ultaid:detail",
                # Need comma at end of kwargs for some picky Django reason
                # https://stackoverflow.com/questions/52575418/reverse-with-prefix-argument-after-must-be-an-iterable-not-int/52575419
                kwargs={
                    "pk": self.object.pk,
                },
            )

    def post(self, request, **kwargs):
        # Uses UpdateView to get the ULTAid instance requested and put it in a form
        form = self.form_class(request.POST, instance=self.get_object())
        # Fetch object's User from the form instance
        self.user = form.instance.user
        # Fetch related models to instantiate related model forms
        CKD_form = self.CKD_form_class(request.POST, instance=self.user.medicalprofile.CKD)
        erosions_form = self.erosions_form_class(request.POST, instance=self.user.medicalprofile.erosions)
        XOI_interactions_form = self.XOI_interactions_form_class(
            request.POST, instance=self.user.medicalprofile.XOI_interactions
        )
        organ_transplant_form = self.organ_transplant_form_class(
            request.POST, instance=self.user.medicalprofile.organ_transplant
        )
        allopurinol_hypersensitivity_form = self.allopurinol_hypersensitivity_form_class(
            request.POST, instance=self.user.medicalprofile.allopurinol_hypersensitivity
        )
        febuxostat_hypersensitivity_form = self.febuxostat_hypersensitivity_form_class(
            request.POST, instance=self.user.medicalprofile.febuxostat_hypersensitivity
        )
        heartattack_form = self.heartattack_form_class(request.POST, instance=self.user.medicalprofile.heartattack)
        stroke_form = self.stroke_form_class(request.POST, instance=self.user.medicalprofile.stroke)
        tophi_form = self.tophi_form_class(request.POST, instance=self.user.medicalprofile.tophi)

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
                    CKD_form=self.CKD_form_class(request.POST, instance=self.user.medicalprofile.CKD),
                    erosions_form=self.erosions_form_class(request.POST, instance=self.user.medicalprofile.erosions),
                    XOI_interactions_form=self.XOI_interactions_form_class(
                        request.POST, instance=self.user.medicalprofile.XOI_interactions
                    ),
                    organ_transplant_form=self.organ_transplant_form_class(
                        request.POST, instance=self.user.medicalprofile.organ_transplant
                    ),
                    allopurinol_hypersensitivity_form=self.allopurinol_hypersensitivity_form_class(
                        request.POST, instance=self.user.medicalprofile.allopurinol_hypersensitivity
                    ),
                    febuxostat_hypersensitivity_form=self.febuxostat_hypersensitivity_form_class(
                        request.POST, instance=self.user.medicalprofile.febuxostat_hypersensitivity
                    ),
                    heartattack_form=self.heartattack_form_class(
                        request.POST, instance=self.user.medicalprofile.heartattack
                    ),
                    stroke_form=self.stroke_form_class(request.POST, instance=self.user.medicalprofile.stroke),
                    tophi_form=self.tophi_form_class(request.POST, instance=self.user.medicalprofile.tophi),
                )
            )
