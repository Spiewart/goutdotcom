from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

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
from ..ultaid.models import ULTAid
from .forms import PPxAidForm
from .models import PPxAid


class PPxAidCreate(CreateView):
    model = PPxAid
    form_class = PPxAidForm
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
        # Check if POST has 'ultaid' kwarg and assign PPxAid OnetoOne related object based on pk='ultaid'
        if self.kwargs.get("ultaid"):
            form.instance.ultaid = ULTAid.objects.get(pk=self.kwargs.get("ultaid"))
            # If user is not authenticated and created a PPxAid from a ULTAid, use ULTAid CKD, HeartAttack, and Stroke instances instead of making new ones, removed forms in form via Kwargs and layout objects
            if self.request.user.is_authenticated == False:
                form.instance.ckd = form.instance.ultaid.ckd
                form.instance.heartattack = form.instance.ultaid.heartattack
                form.instance.stroke = form.instance.ultaid.stroke
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Checks if User is authenticated and redirects to PPxAid UpdateView if so
        if self.request.user.is_authenticated:
            try:
                user_PPxAid = self.model.objects.get(user=self.request.user)
            except self.model.DoesNotExist:
                user_PPxAid = None
            if user_PPxAid:
                return redirect("ppxaid:update", pk=user_PPxAid.pk)
            else:
                return super().get(request, *args, **kwargs)
        else:
            if "ultaid" in kwargs:
                try:
                    ultaid = ULTAid.objects.get(pk=kwargs["ultaid"])
                    ultaid_PPxAid = self.model.objects.get(ultaid=ultaid)
                except self.model.DoesNotExist:
                    ultaid_PPxAid = None
                if ultaid_PPxAid:
                    return redirect("ppxaid:detail", pk=ultaid.ppxaid.pk)
                else:
                    return super().get(request, *args, **kwargs)
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PPxAidCreate, self).get_context_data(**kwargs)
        # Add FlareAid OnetoOne related model objects from the MedicalProfile for the logged in User
        if self.request.user.is_authenticated:
            if "anticoagulation_form" not in context:
                context["anticoagulation_form"] = self.anticoagulation_form_class(
                    instance=self.request.user.medicalprofile.anticoagulation
                )
            if "bleed_form" not in context:
                context["bleed_form"] = self.bleed_form_class(instance=self.request.user.medicalprofile.bleed)
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.request.user.medicalprofile.CKD)
            if "colchicine_interactions_form" not in context:
                context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                    instance=self.request.user.medicalprofile.colchicine_interactions
                )
            if "diabetes_form" not in context:
                context["diabetes_form"] = self.diabetes_form_class(instance=self.request.user.medicalprofile.diabetes)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    instance=self.request.user.medicalprofile.heartattack
                )
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(instance=self.request.user.medicalprofile.IBD)
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(
                    instance=self.request.user.medicalprofile.osteoporosis
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.request.user.medicalprofile.stroke)
            return context
        else:
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
            return context

    def get_form_kwargs(self):
        """Ovewrites get_form_kwargs() to look for 'ultaid' kwarg in GET request, uses 'ultaid' to query database for associated ULTAid for use in PPxAidForm
        returns: [dict: dict containing 'ultaid' kwarg for form]"""
        # Assign self.ultaid from GET request kwargs before calling super() which will overwrite kwargs
        self.ultaid = self.kwargs.get("ultaid", None)
        self.no_user = False
        if self.request.user.is_authenticated == False:
            self.no_user = True
        kwargs = super(PPxAidCreate, self).get_form_kwargs()
        # Checks if flare kwarg came from ULTAid Detail and queries database for ultaid_pk that matches self.ultaid from initial kwargs
        if self.ultaid:
            ultaid_pk = self.ultaid
            ultaid = ULTAid.objects.get(pk=ultaid_pk)
            kwargs["ultaid"] = ultaid
            kwargs["no_user"] = self.no_user
            # If User is anonymous / not logged in and PPxAid has a ULTAid, pass ckd stroke and heartattack from ULTAid to PPxAid to avoid duplication of user input
            if self.request.user.is_authenticated == False:
                kwargs["ckd"] = ultaid.stroke
                kwargs["stroke"] = ultaid.stroke
                kwargs["heartattack"] = ultaid.heartattack
        return kwargs

    def get_success_url(self):
        if self.kwargs.get("ultaid"):
            return reverse("ultaid:detail", kwargs={"pk": self.kwargs["ultaid"]})
        else:
            return reverse(
                "ppxaid:detail",
                # Need comma at end of kwargs for some picky Django reason
                # https://stackoverflow.com/questions/52575418/reverse-with-prefix-argument-after-must-be-an-iterable-not-int/52575419
                kwargs={
                    "pk": self.object.pk,
                },
            )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=PPxAid())
        ppxaid_data = form.save(commit=False)
        if request.user.is_authenticated:
            # Check if user is authenticated and pull OnetoOne related model data from MedicalProfile if so
            ppxaid_data.user = request.user
            anticoagulation_form = self.anticoagulation_form_class(
                request.POST, instance=request.user.medicalprofile.anticoagulation
            )
            bleed_form = self.bleed_form_class(request.POST, instance=request.user.medicalprofile.bleed)
            CKD_form = self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD)
            colchicine_interactions_form = self.colchicine_interactions_form_class(
                request.POST, instance=request.user.medicalprofile.colchicine_interactions
            )
            diabetes_form = self.diabetes_form_class(request.POST, instance=request.user.medicalprofile.diabetes)
            heartattack_form = self.heartattack_form_class(
                request.POST, instance=request.user.medicalprofile.heartattack
            )
            IBD_form = self.IBD_form_class(request.POST, instance=request.user.medicalprofile.IBD)
            osteoporosis_form = self.osteoporosis_form_class(
                request.POST, instance=request.user.medicalprofile.osteoporosis
            )
            stroke_form = self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke)
        else:
            # If not logged in show forms for new History objects without User
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
            # Need to call form_valid(), not redirect. form_valid() super function returns to object DetailView
            return self.form_valid(form)
        else:
            if request.user.is_authenticated:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        anticoagulation_form=self.anticoagulation_form_class(
                            request.POST, instance=request.user.medicalprofile.anticoagulation
                        ),
                        bleed_form=self.bleed_form_class(request.POST, instance=request.user.medicalprofile.bleed),
                        CKD_form=self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD),
                        colchicine_interactions_form=self.colchicine_interactions_form_class(
                            request.POST, instance=request.user.medicalprofile.colchicine_interactions
                        ),
                        diabetes_form=self.diabetes_form_class(
                            request.POST, instance=request.user.medicalprofile.diabetes
                        ),
                        heartattack_form=self.heartattack_form_class(
                            request.POST, instance=request.user.medicalprofile.heartattack
                        ),
                        IBD_form=self.IBD_form_class(request.POST, instance=request.user.medicalprofile.IBD),
                        osteoporosis_form=self.osteoporosis_form_class(
                            request.POST, instance=request.user.medicalprofile.osteoporosis
                        ),
                        stroke_form=self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke),
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


class PPxAidDetail(DetailView):
    model = PPxAid
    template_name = "ppxaid/ppxaid_detail.html"


class PPxAidUpdate(LoginRequiredMixin, UpdateView):
    model = PPxAid
    form_class = PPxAidForm
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
        # Check if POST has 'ultaid' kwarg and assign PPxAid ULTAid OnetoOne related object based on pk='ultaid'
        if self.kwargs.get("ultaid"):
            form.instance.ultaid = ULTAid.objects.get(pk=self.kwargs.get("ultaid"))
        # For updating, check if user has created a PPxTreatment model object out of previous iteration of PPxAid, if so, delete it
        try:
            form.instance.colchicine.delete()
        except ObjectDoesNotExist:
            pass
        try:
            form.instance.ibuprofen.delete()
        except ObjectDoesNotExist:
            pass
        try:
            form.instance.prednisone.delete()
        except ObjectDoesNotExist:
            pass
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PPxAidUpdate, self).get_context_data(**kwargs)
        # Add PPxAid OnetoOne related model objects from the MedicalProfile for the logged in User
        if self.request.POST:
            if "anticoagulation_form" not in context:
                context["anticoagulation_form"] = self.anticoagulation_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.anticoagulation
                )
            if "bleed_form" not in context:
                context["bleed_form"] = self.bleed_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.bleed
                )
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.CKD
                )
            if "colchicine_interactions_form" not in context:
                context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.colchicine_interactions
                )
            if "diabetes_form" not in context:
                context["diabetes_form"] = self.diabetes_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.diabetes
                )
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.heartattack
                )
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.IBD
                )
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.osteoporosis
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(
                    self.request.POST, instance=self.request.user.medicalprofile.stroke
                )
            return context
        else:
            if "anticoagulation_form" not in context:
                context["anticoagulation_form"] = self.anticoagulation_form_class(
                    instance=self.request.user.medicalprofile.anticoagulation
                )
            if "bleed_form" not in context:
                context["bleed_form"] = self.bleed_form_class(instance=self.request.user.medicalprofile.bleed)
            if "CKD_form" not in context:
                context["CKD_form"] = self.CKD_form_class(instance=self.request.user.medicalprofile.CKD)
            if "colchicine_interactions_form" not in context:
                context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                    instance=self.request.user.medicalprofile.colchicine_interactions
                )
            if "diabetes_form" not in context:
                context["diabetes_form"] = self.diabetes_form_class(instance=self.request.user.medicalprofile.diabetes)
            if "heartattack_form" not in context:
                context["heartattack_form"] = self.heartattack_form_class(
                    instance=self.request.user.medicalprofile.heartattack
                )
            if "IBD_form" not in context:
                context["IBD_form"] = self.IBD_form_class(instance=self.request.user.medicalprofile.IBD)
            if "osteoporosis_form" not in context:
                context["osteoporosis_form"] = self.osteoporosis_form_class(
                    instance=self.request.user.medicalprofile.osteoporosis
                )
            if "stroke_form" not in context:
                context["stroke_form"] = self.stroke_form_class(instance=self.request.user.medicalprofile.stroke)
            return context

    def get_form_kwargs(self):
        """Overwrites get_form_kwargs() to look for 'ultaid' kwarg in GET request, uses 'ultaid' to query database for associated ULTAid for use in PPxAidForm
        returns: [dict: dict containing 'ultaid' kwarg for form]"""
        # Assign self.ultaid from GET request kwargs before calling super() which will overwrite kwargs
        self.ultaid = self.kwargs.get("ultaid", None)
        kwargs = super(PPxAidUpdate, self).get_form_kwargs()
        # Checks if ultaid kwarg came from ULTAid Detail and queries database for ultaid_pk that matches self.ultaid from initial kwargs
        if self.ultaid:
            ultaid_pk = self.ultaid
            ultaid = ULTAid.objects.get(pk=ultaid_pk)
            kwargs["ultaid"] = ultaid
        return kwargs

    def post(self, request, *args, **kwargs):
        # Uses UpdateView to get the PPxAid instance requested and put it in a form
        form = self.form_class(request.POST, instance=self.get_object())
        anticoagulation_form = self.anticoagulation_form_class(
            request.POST, instance=request.user.medicalprofile.anticoagulation
        )
        bleed_form = self.bleed_form_class(request.POST, instance=request.user.medicalprofile.bleed)
        CKD_form = self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD)
        colchicine_interactions_form = self.colchicine_interactions_form_class(
            request.POST, instance=request.user.medicalprofile.colchicine_interactions
        )
        diabetes_form = self.diabetes_form_class(request.POST, instance=request.user.medicalprofile.diabetes)
        heartattack_form = self.heartattack_form_class(request.POST, instance=request.user.medicalprofile.heartattack)
        IBD_form = self.IBD_form_class(request.POST, instance=request.user.medicalprofile.IBD)
        osteoporosis_form = self.osteoporosis_form_class(
            request.POST, instance=request.user.medicalprofile.osteoporosis
        )
        stroke_form = self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke)

        if form.is_valid():
            ppxaid_data = form.save(commit=False)
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
            ppxaid_data.anticoagulation = anticoagulation_data
            ppxaid_data.bleed = bleed_data
            ppxaid_data.ckd = ckd_data
            ppxaid_data.colchicine_interactions = colchicine_interactions_data
            ppxaid_data.diabetes = diabetes_data
            ppxaid_data.heartattack = heartattack_data
            ppxaid_data.ibd = IBD_data
            ppxaid_data.osteoporosis = osteoporosis_data
            ppxaid_data.stroke = stroke_data
            # Need to call form_valid(), not redirect. form_valid() super function returns to object DetailView
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    anticoagulation_form=self.anticoagulation_form_class(
                        request.POST, instance=request.user.medicalprofile.anticoagulation
                    ),
                    bleed_form=self.bleed_form_class(request.POST, instance=request.user.medicalprofile.bleed),
                    CKD_form=self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD),
                    colchicine_interactions_form=self.colchicine_interactions_form_class(
                        request.POST, instance=request.user.medicalprofile.colchicine_interactions
                    ),
                    diabetes_form=self.diabetes_form_class(request.POST, instance=request.user.medicalprofile.diabetes),
                    heartattack_form=self.heartattack_form_class(
                        request.POST, instance=request.user.medicalprofile.heartattack
                    ),
                    IBD_form=self.IBD_form_class(request.POST, instance=request.user.medicalprofile.IBD),
                    osteoporosis_form=self.osteoporosis_form_class(
                        request.POST, instance=request.user.medicalprofile.osteoporosis
                    ),
                    stroke_form=self.stroke_form_class(request.POST, instance=request.user.medicalprofile.stroke),
                )
            )
