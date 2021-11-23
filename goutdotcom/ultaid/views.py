from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from ..history.forms import (
    AllopurinolHypersensitivitySimpleForm,
    CKDForm,
    FebuxostatHypersensitivitySimpleForm,
    HeartAttackSimpleForm,
    OrganTransplantForm,
    StrokeForm,
    StrokeSimpleForm,
    XOIInteractionsSimpleForm,
)
from ..history.models import (
    CKD,
    AllopurinolHypersensitivity,
    FebuxostatHypersensitivity,
    HeartAttack,
    OrganTransplant,
    Stroke,
    XOIInteractions,
)
from ..ult.models import ULT
from .forms import ULTAidForm
from .models import ULTAid

# Create your views here.


class ULTAidCreate(CreateView):
    model = ULTAid
    form_class = ULTAidForm
    CKD_form_class = CKDForm
    XOI_interactions_form_class = XOIInteractionsSimpleForm
    organ_transplant_form_class = OrganTransplantForm
    allopurinol_hypersensitivity_form_class = AllopurinolHypersensitivitySimpleForm
    febuxostat_hypersensitivity_form_class = FebuxostatHypersensitivitySimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    stroke_form_class = StrokeSimpleForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Checks if user is logged in, if they have already created a ULTAid, and redirects to UpdateView if so
        if self.request.user.is_authenticated:
            try:
                user_ULTAid = self.model.objects.get(user=self.request.user)
            except self.model.DoesNotExist:
                user_ULTAid = None
            if user_ULTAid:
                return redirect("ultaid:update", pk=self.model.objects.get(user=self.request.user).pk)
            else:
                return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ULTAidCreate, self).get_context_data(**kwargs)
        ## IS IF NOT IN CONTEXT STATEMENT NECESSARY? TEST IT BY DELETING
        ## WHAT IF USER IS NOT LOGGED IN? CHECK CONTEXT
        # Add ULTAid OnetoOne related model objects from the MedicalProfile for the logged in User
        if self.request.user.is_anonymous == False:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.request.user.medicalprofile.CKD)
            if "XOI_interactions_form" not in context:
                context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                    instance=self.request.user.medicalprofile.XOI_interactions
                )
            if "organ_transplant_form" not in context:
                context["organ_transplant_form"] = self.organ_transplant_form_class(
                    instance=self.request.user.medicalprofile.organ_transplant
                )
            if "allopurinol_hypersensitivity_form" not in context:
                context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                    instance=self.request.user.medicalprofile.allopurinol_hypersensitivity
                )
            if "febuxostat_hypersensitivity_form" not in context:
                context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                    instance=self.request.user.medicalprofile.febuxostat_hypersensitivity
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    instance=self.request.user.medicalprofile.heartattack
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.request.user.medicalprofile.stroke)
            return context
        else:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(self.request.GET)
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
            return context

    def post(self, request):
        form = self.form_class(request.POST, instance=ULTAid())

        if form.is_valid():
            ULTAid_data = form.save(commit=False)
            ## WOULD LIKE TO CONSOLIDATE REQUEST.USER ADD TO RIGHT BEFORE SAVE(), THEN CAN COMBINE THE REST
            # Check if user is authenticated and pull OnetoOne related model data from MedicalProfile if so
            if request.user.is_authenticated:
                ULTAid_data.user = request.user
                CKD_form = self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD)
                CKD_data = CKD_form.save(commit=False)
                CKD_data.last_modified = "ULTAid"
                CKD_data.save()
                XOI_interactions_form = self.XOI_interactions_form_class(
                    request.POST, instance=request.user.medicalprofile.XOI_interactions
                )
                XOI_interactions_data = XOI_interactions_form.save(commit=False)
                XOI_interactions_data.last_modified = "ULTAid"
                XOI_interactions_data.save()
                organ_transplant_form = self.organ_transplant_form_class(
                    request.POST, instance=request.user.medicalprofile.organ_transplant
                )
                organ_transplant_data = organ_transplant_form.save(commit=False)
                organ_transplant_data.last_modified = "ULTAid"
                organ_transplant_data.save()
                allopurinol_hypersensitivity_form = self.allopurinol_hypersensitivity_form_class(
                    request.POST, instance=request.user.medicalprofile.allopurinol_hypersensitivity
                )
                allopurinol_hypersensitivity_data = allopurinol_hypersensitivity_form.save(commit=False)
                allopurinol_hypersensitivity_data.last_modified = "ULTAid"
                allopurinol_hypersensitivity_data.save()
                febuxostat_hypersensitivity_form = self.febuxostat_hypersensitivity_form_class(
                    request.POST, instance=request.user.medicalprofile.febuxostat_hypersensitivity
                )
                febuxostat_hypersensitivity_data = febuxostat_hypersensitivity_form.save(commit=False)
                febuxostat_hypersensitivity_data.last_modified = "ULTAid"
                febuxostat_hypersensitivity_data.save()
                heartattack_form = self.heartattack_form_class(
                    request.POST, instance=request.user.medicalprofile.heartattack
                )
                heartattack_data = heartattack_form.save(commit=False)
                heartattack_data.last_modified = "ULTAid"
                heartattack_data.save()
                stroke_form = self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke)
                stroke_data = stroke_form.save(commit=False)
                stroke_data.last_modified = "ULTAid"
                stroke_data.save()
                ULTAid_data.ckd = CKD_data
                ULTAid_data.XOI_interactions = XOI_interactions_data
                ULTAid_data.organ_transplant = organ_transplant_data
                ULTAid_data.allopurinol_hypersensitivity = allopurinol_hypersensitivity_data
                ULTAid_data.febuxostat_hypersensitivity = febuxostat_hypersensitivity_data
                ULTAid_data.heartattack = heartattack_data
                ULTAid_data.stroke = stroke_data
                ULTAid_data.save()
            else:
                CKD_form = self.CKD_form_class(request.POST, instance=CKD())
                CKD_data = CKD_form.save(commit=False)
                CKD_data.last_modified = "ULTAid"
                CKD_data.save()
                XOI_interactions_form = self.XOI_interactions_form_class(request.POST, instance=XOIInteractions())
                XOI_interactions_data = XOI_interactions_form.save(commit=False)
                XOI_interactions_data.last_modified = "ULTAid"
                XOI_interactions_data.save()
                organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=OrganTransplant())
                organ_transplant_data = organ_transplant_form.save(commit=False)
                organ_transplant_data.last_modified = "ULTAid"
                organ_transplant_data.save()
                allopurinol_hypersensitivity_form = self.allopurinol_hypersensitivity_form_class(
                    request.POST, instance=AllopurinolHypersensitivity()
                )
                allopurinol_hypersensitivity_data = allopurinol_hypersensitivity_form.save(commit=False)
                allopurinol_hypersensitivity_data.last_modified = "ULTAid"
                allopurinol_hypersensitivity_data.save()
                febuxostat_hypersensitivity_form = self.febuxostat_hypersensitivity_form_class(
                    request.POST, instance=FebuxostatHypersensitivity()
                )
                febuxostat_hypersensitivity_data = febuxostat_hypersensitivity_form.save(commit=False)
                febuxostat_hypersensitivity_data.last_modified = "ULTAid"
                febuxostat_hypersensitivity_data.save()
                heartattack_form = self.heartattack_form_class(request.POST, instance=HeartAttack())
                heartattack_data = heartattack_form.save(commit=False)
                heartattack_data.last_modified = "ULTAid"
                heartattack_data.save()
                stroke_form = self.stroke_form_class(request.POST, instance=Stroke())
                stroke_data = stroke_form.save(commit=False)
                stroke_data.last_modified = "ULTAid"
                stroke_data.save()
                ULTAid_data.ckd = CKD_data
                ULTAid_data.XOI_interactions = XOI_interactions_data
                ULTAid_data.organ_transplant = organ_transplant_data
                ULTAid_data.allopurinol_hypersensitivity = allopurinol_hypersensitivity_data
                ULTAid_data.febuxostat_hypersensitivity = febuxostat_hypersensitivity_data
                ULTAid_data.heartattack = heartattack_data
                ULTAid_data.stroke = stroke_data
                ULTAid_data.save()
            return HttpResponseRedirect(reverse("ultaid:detail", kwargs={"pk": ULTAid_data.pk}))
        else:
            if request.user.is_authenticated:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        CKD_form=self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD),
                        XOI_interactions_form=self.XOI_interactions_form_class(
                            request.POST, instance=request.user.medicalprofile.XOI_interactions
                        ),
                        organ_transplant_form=self.organ_transplant_form_class(
                            request.POST, instance=request.user.medicalprofile.organ_transplant
                        ),
                        allopurinol_hypersensitivity_form=self.allopurinol_hypersensitivity_form_class(
                            request.POST, instance=request.user.medicalprofile.allopurinol_hypersensitivity
                        ),
                        febuxostat_hypersensitivity_form=self.febuxostat_hypersensitivity_form_class(
                            request.POST, instance=request.user.medicalprofile.febuxostat_hypersensitivity
                        ),
                        heartattack_form=self.heartattack_form_class(
                            request.POST, instance=request.user.medicalprofile.heartattack
                        ),
                        stroke_form=self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke),
                    )
                )
            else:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        CKD_form=self.CKD_form_class(request.POST, instance=CKD()),
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
                    )
                )


class ULTAidDetail(DetailView):
    model = ULTAid


class ULTAidUpdate(LoginRequiredMixin, UpdateView):
    model = ULTAid
    form_class = ULTAidForm
    CKD_form_class = CKDForm
    XOI_interactions_form_class = XOIInteractionsSimpleForm
    organ_transplant_form_class = OrganTransplantForm
    allopurinol_hypersensitivity_form_class = AllopurinolHypersensitivitySimpleForm
    febuxostat_hypersensitivity_form_class = FebuxostatHypersensitivitySimpleForm
    heartattack_form_class = HeartAttackSimpleForm
    stroke_form_class = StrokeSimpleForm

    def get_context_data(self, **kwargs):
        context = super(ULTAidUpdate, self).get_context_data(**kwargs)
        # Adds appropriate OnetoOne related History/MedicalProfile model forms to context
        if self.request.POST:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.CKD
                )
            if "XOI_interactions_form" not in context:
                context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.XOI_interactions
                )
            if "organ_transplant_form" not in context:
                context["organ_transplant_form"] = self.organ_transplant_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.organ_transplant
                )
            if "allopurinol_hypersensitivity_form" not in context:
                context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.allopurinol_hypersensitivity
                )
            if "febuxostat_hypersensitivity_form" not in context:
                context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.febuxostat_hypersensitivity
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.heartattack
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.stroke
                )
            # Check if user is logged in, pass ULT results to ULTAid view/context for JQuery evaluation to update form fields
            #### IS THIS NEEDED FOR POST?
            if self.request.user.is_authenticated:
                if self.request.user.ult:
                    context["user_ult"] = ULT.objects.get(user=self.request.user).calculator()
            return context
        else:
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.request.user.medicalprofile.CKD)
            if "XOI_interactions_form" not in context:
                context["XOI_interactions_form"] = self.XOI_interactions_form_class(
                    instance=self.request.user.medicalprofile.XOI_interactions
                )
            if "organ_transplant_form" not in context:
                context["organ_transplant_form"] = self.organ_transplant_form_class(
                    instance=self.request.user.medicalprofile.organ_transplant
                )
            if "allopurinol_hypersensitivity_form" not in context:
                context["allopurinol_hypersensitivity_form"] = self.allopurinol_hypersensitivity_form_class(
                    instance=self.request.user.medicalprofile.allopurinol_hypersensitivity
                )
            if "febuxostat_hypersensitivity_form" not in context:
                context["febuxostat_hypersensitivity_form"] = self.febuxostat_hypersensitivity_form_class(
                    instance=self.request.user.medicalprofile.febuxostat_hypersensitivity
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    instance=self.request.user.medicalprofile.heartattack
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.request.user.medicalprofile.stroke)
            # Check if user is logged in, pass ULT results to ULTAid view/context for JQuery evaluation to update form fields
            if self.request.user.is_authenticated:
                if self.request.user.ult:
                    context["user_ult"] = ULT.objects.get(user=self.request.user).calculator()
            return context

    def post(self, request, **kwargs):
        # Uses UpdateView to get the ULTAid instance requested and put it in a form
        form = self.form_class(request.POST, instance=self.get_object())
        CKD_form = self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD)
        XOI_interactions_form = self.XOI_interactions_form_class(
            request.POST, instance=request.user.medicalprofile.XOI_interactions
        )
        organ_transplant_form = self.organ_transplant_form_class(
            request.POST, instance=request.user.medicalprofile.organ_transplant
        )
        allopurinol_hypersensitivity_form = self.allopurinol_hypersensitivity_form_class(
            request.POST, instance=request.user.medicalprofile.allopurinol_hypersensitivity
        )
        febuxostat_hypersensitivity_form = self.febuxostat_hypersensitivity_form_class(
            request.POST, instance=request.user.medicalprofile.febuxostat_hypersensitivity
        )
        heartattack_form = self.heartattack_form_class(request.POST, instance=request.user.medicalprofile.heartattack)
        stroke_form = self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke)

        if form.is_valid():
            # Uses related OnetoOne field forms to populate ULTAid fields, changes last_modified to ULTAid, and saves all data
            ULTAid_data = form.save(commit=False)
            CKD_data = CKD_form.save(commit=False)
            CKD_data.last_modified = "ULTAid"
            CKD_data.save()
            XOI_interactions_data = XOI_interactions_form.save(commit=False)
            XOI_interactions_data.last_modified = "ULTAid"
            XOI_interactions_data.save()
            organ_transplant_data = organ_transplant_form.save(commit=False)
            organ_transplant_data.last_modified = "ULTAid"
            organ_transplant_data.save()
            allopurinol_hypersensitivity_data = allopurinol_hypersensitivity_form.save(commit=False)
            allopurinol_hypersensitivity_data.last_modified = "ULTAid"
            allopurinol_hypersensitivity_data.save()
            febuxostat_hypersensitivity_data = febuxostat_hypersensitivity_form.save(commit=False)
            febuxostat_hypersensitivity_data.last_modified = "ULTAid"
            febuxostat_hypersensitivity_data.save()
            heartattack_data = heartattack_form.save(commit=False)
            heartattack_data.last_modified = "ULTAid"
            heartattack_data.save()
            stroke_data = stroke_form.save(commit=False)
            stroke_data.last_modified = "ULTAid"
            stroke_data.save()
            ULTAid_data.ckd = CKD_data
            ULTAid_data.XOI_interactions = XOI_interactions_data
            ULTAid_data.organ_transplant = organ_transplant_data
            ULTAid_data.allopurinol_hypersensitivity = allopurinol_hypersensitivity_data
            ULTAid_data.febuxostat_hypersensitivity = febuxostat_hypersensitivity_data
            ULTAid_data.heartattack = heartattack_data
            ULTAid_data.stroke = stroke_data
            ULTAid_data.save()
            return HttpResponseRedirect(reverse("ultaid:detail", kwargs={"pk": ULTAid_data.pk}))
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    CKD_form=self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD),
                    XOI_interactions_form=self.XOI_interactions_form_class(
                        request.POST, instance=request.user.medicalprofile.XOI_interactions
                    ),
                    organ_transplant_form=self.organ_transplant_form_class(
                        request.POST, instance=request.user.medicalprofile.organ_transplant
                    ),
                    allopurinol_hypersensitivity_form=self.allopurinol_hypersensitivity_form_class(
                        request.POST, instance=request.user.medicalprofile.allopurinol_hypersensitivity
                    ),
                    febuxostat_hypersensitivity_form=self.febuxostat_hypersensitivity_form_class(
                        request.POST, instance=request.user.medicalprofile.febuxostat_hypersensitivity
                    ),
                    heartattack_form=self.heartattack_form_class(
                        request.POST, instance=request.user.medicalprofile.heartattack
                    ),
                    stroke_form=self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke),
                )
            )
