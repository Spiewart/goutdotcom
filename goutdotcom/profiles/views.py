from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.views.generic import CreateView, UpdateView

from goutdotcom.history.forms import (
    AlcoholForm,
    BleedForm,
    CHFForm,
    CKDForm,
    DiabetesForm,
    ErosionsForm,
    FructoseForm,
    GoutForm,
    HeartAttackForm,
    HypertensionForm,
    HyperuricemiaForm,
    OrganTransplantForm,
    ShellfishForm,
    StrokeForm,
    TophiForm,
    UrateKidneyStonesForm,
)
from goutdotcom.history.models import (
    CHF,
    CKD,
    Alcohol,
    Bleed,
    Diabetes,
    Erosions,
    Fructose,
    Gout,
    HeartAttack,
    Hypertension,
    Hyperuricemia,
    OrganTransplant,
    Shellfish,
    Stroke,
    Tophi,
    UrateKidneyStones,
)
from goutdotcom.profiles.forms import (
    ContraindicationsProfileForm,
    FamilyProfileForm,
    MedicalProfileForm,
    PatientProfileForm,
    SocialProfileForm,
)
from goutdotcom.vitals.forms import HeightForm, WeightForm
from goutdotcom.vitals.models import Height, Weight

from .models import (
    ContraindicationsProfile,
    FamilyProfile,
    MedicalProfile,
    PatientProfile,
    SocialProfile,
)


# Mixins
class AssignUserMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserDetailRedirectMixin:
    def get_success_url(self):
        return self.request.user.get_absolute_url()


# Create your views here.
class ContraindicationsProfileCreate(LoginRequiredMixin, AssignUserMixin, UserDetailRedirectMixin, CreateView):
    model = ContraindicationsProfile
    form_class = ContraindicationsProfileForm
    stroke_form_class = StrokeForm
    heartattack_form_class = HeartAttackForm
    bleed_form_class = BleedForm

    def get_context_data(self, **kwargs):
        context = super(ContraindicationsProfileCreate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if "stroke_form" not in context:
            context["stroke_form"] = self.stroke_form_class(self.request.GET)
        if "heartattack_form" not in context:
            context["heartattack_form"] = self.heartattack_form_class(self.request.GET)
        if "bleed_form" not in context:
            context["bleed_form"] = self.bleed_form_class(self.request.GET)
        return context

    def get_object(self, queryset=None):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=ContraindicationsProfile())
        stroke_form = self.stroke_form_class(request.POST, instance=Stroke())
        heartattack_form = self.heartattack_form_class(request.POST, instance=HeartAttack())
        bleed_form = self.bleed_form_class(request.POST, instance=Bleed())

        if form.is_valid() and stroke_form.is_valid() and heartattack_form.is_valid() and bleed_form.is_valid():
            contraindications_profile_data = form.save(commit=False)
            contraindications_profile_data.user = request.user
            stroke_data = stroke_form.save(commit=False)
            stroke_data.user = request.user
            stroke_data.save()
            heartattack_data = heartattack_form.save(commit=False)
            heartattack_data.user = request.user
            heartattack_data.save()
            bleed_data = bleed_form.save(commit=False)
            bleed_data.user = request.user
            bleed_data.save()
            contraindications_profile_data.stroke = stroke_data
            contraindications_profile_data.heartattack = heartattack_data
            contraindications_profile_data.bleed = bleed_data
            contraindications_profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    stroke_form=stroke_form,
                    heartattack_form=heartattack_form,
                    bleed_form=bleed_form,
                )
            )


class ContraindicationsProfileUpdate(LoginRequiredMixin, AssignUserMixin, UserDetailRedirectMixin, UpdateView):
    model = ContraindicationsProfile
    form_class = ContraindicationsProfileForm
    stroke_form_class = StrokeForm
    heartattack_form_class = HeartAttackForm
    bleed_form_class = BleedForm

    def get_context_data(self, **kwargs):
        context = super(ContraindicationsProfileUpdate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if self.request.POST:
            context["stroke_form"] = StrokeForm(self.request.POST, instance=self.object.stroke)
            context["heartattack_form"] = HeartAttackForm(self.request.POST, instance=self.object.heartattack)
            context["bleed_form"] = BleedForm(self.request.POST, instance=self.object.bleed)
        else:
            context["stroke_form"] = self.stroke_form_class(instance=self.object.stroke)
            context["heartattack_form"] = self.heartattack_form_class(instance=self.object.heartattack)
            context["bleed_form"] = self.bleed_form_class(instance=self.object.bleed)
        return context

    def get_object(self, queryset=None):
        try:
            queryset = self.model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(ContraindicationsProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        # NEED **kwargs even though VSCode IDE says it's not used. Can't accept <user> and <pk> from url parameter otherwise.
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        stroke_form = self.stroke_form_class(request.POST, instance=self.object.stroke)
        heartattack_form = self.heartattack_form_class(request.POST, instance=self.object.heartattack)
        bleed_form = self.bleed_form_class(request.POST, instance=self.object.bleed)

        if form.is_valid() and stroke_form.is_valid() and heartattack_form.is_valid() and bleed_form.is_valid():
            contraindications_profile_data = form.save(commit=False)
            stroke_data = stroke_form.save()
            heartattack_data = heartattack_form.save()
            bleed_data = bleed_form.save()
            contraindications_profile_data.ckd = stroke_data
            contraindications_profile_data.hypertension = heartattack_data
            contraindications_profile_data.bleed = bleed_data
            contraindications_profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    stroke_form=stroke_form,
                    heartattack_form=heartattack_form,
                    bleed_form=bleed_form,
                )
            )


class FamilyProfileCreate(LoginRequiredMixin, AssignUserMixin, UserDetailRedirectMixin, CreateView):
    model = FamilyProfile
    form_class = FamilyProfileForm
    gout_form_class = GoutForm

    def get_context_data(self, **kwargs):
        context = super(FamilyProfileCreate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if "gout_form" not in context:
            context["gout_form"] = self.gout_form_class(self.request.GET)
        return context

    def get_object(self, queryset=None):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=FamilyProfile())
        gout_form = self.gout_form_class(request.POST, instance=Gout())

        if form.is_valid() and gout_form.is_valid():
            family_profile_data = form.save(commit=False)
            family_profile_data.user = request.user
            gout_data = gout_form.save(commit=False)
            gout_data.user = request.user
            gout_data.save()
            family_profile_data.gout = gout_data
            family_profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    gout_form=gout_form,
                )
            )


class FamilyProfileUpdate(LoginRequiredMixin, AssignUserMixin, UserDetailRedirectMixin, UpdateView):
    model = FamilyProfile
    form_class = FamilyProfileForm
    gout_form_class = GoutForm

    def get_context_data(self, **kwargs):
        context = super(FamilyProfileUpdate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if self.request.POST:
            context["gout_form"] = GoutForm(self.request.POST, instance=self.object.gout)
        else:
            context["gout_form"] = self.gout_form_class(instance=self.object.gout)
        return context

    def get_object(self, queryset=None):
        try:
            queryset = self.model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(FamilyProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        # NEED **kwargs even though VSCode IDE says it's not used. Can't accept <user> and <pk> from url parameter otherwise.
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        gout_form = self.gout_form_class(request.POST, instance=self.object.gout)

        if form.is_valid() and gout_form.is_valid():
            family_profile_data = form.save(commit=False)
            gout_data = gout_form.save()
            family_profile_data.gout = gout_data
            family_profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    gout_form=gout_form,
                )
            )


class MedicalProfileCreate(LoginRequiredMixin, AssignUserMixin, CreateView):
    model = MedicalProfile
    form_class = MedicalProfileForm
    CKD_form_class = CKDForm
    hypertension_form_class = HypertensionForm
    hyperuricemia_form_class = HyperuricemiaForm
    CHF_form_class = CHFForm
    diabetes_form_class = DiabetesForm
    erosions_form_class = ErosionsForm
    organ_transplant_form_class = OrganTransplantForm
    urate_kidney_stone_form_class = UrateKidneyStonesForm
    tohpi_form_class = TophiForm

    def get_context_data(self, **kwargs):
        context = super(MedicalProfileCreate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if "CHF_form" not in context:
            context["CHF_form"] = self.CHF_form_class(self.request.GET)
        if "CKD_form" not in context:
            context["CKD_form"] = self.CKD_form_class(self.request.GET)
        if "diabetes_form" not in context:
            context["diabetes_form"] = self.erosions_form_class(self.request.GET)
        if "erosions_form" not in context:
            context["erosions_form"] = self.erosions_form_class(self.request.GET)
        if "hypertension_form" not in context:
            context["hypertension_form"] = self.hyperuricemia_form_class(self.request.GET)
        if "hyperuricemia_form" not in context:
            context["hyperuricemia_form"] = self.hyperuricemia_form_class(self.request.GET)
        if "organ_transplant_form" not in context:
            context["organ_transplant_form"] = self.organ_transplant_form_class(self.request.GET)
        if "urate_kidney_stones_form" not in context:
            context["urate_kidney_stones_form"] = self.tophi_form_class(self.request.GET)
        if "tophi_form" not in context:
            context["tophi_form"] = self.tophi_form_class(self.request.GET)
        return context

    def get_object(self, queryset=None):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=MedicalProfile())
        CHF_form = self.CHF_form_class(request.POST, instance=CHF())
        CKD_form = self.CKD_form_class(request.POST, instance=CKD())
        diabetes_form = self.diabetes_form_class(request.POST, instance=Diabetes())
        erosions_form = self.erosions_form_class(request.POST, instance=Erosions())
        hypertension_form = self.hypertension_form_class(request.POST, instance=Hypertension())
        hyperuricemia_form = self.hyperuricemia_form_class(request.POST, instance=Hyperuricemia())
        organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=OrganTransplant())
        urate_kidney_stones_form = self.urate_kidney_stone_form_class(request.POST, instance=UrateKidneyStones())
        tophi_form = self.tohpi_form_class(request.POST, instance=Tophi())

        if (
            form.is_valid()
            and CHF_form.is_valid()
            and CKD_form.is_valid()
            and diabetes_form.is_valid()
            and erosions_form.is_valid()
            and hypertension_form.is_valid()
            and hypertension_form.is_valid()
            and organ_transplant_form.is_valid()
            and urate_kidney_stones_form.is_valid()
            and tophi_form.is_valid()
        ):
            medical_profile_data = form.save(commit=False)
            medical_profile_data.user = request.user
            CHF_data = CHF_form.save(commit=False)
            CHF_data.last_modified = "MedicalProfile"
            CHF_data.user = request.user
            CHF_data.save()
            CKD_data = CKD_form.save(commit=False)
            CKD_data.last_modified = "MedicalProfile"
            CKD_data.user = request.user
            CKD_data.save()
            diabetes_data = diabetes_form.save(commit=False)
            diabetes_data.last_modified = "MedicalProfile"
            diabetes_data.user = request.user
            diabetes_data.save()
            erosions_data = erosions_form.save(commit=False)
            erosions_data.last_modified = "MedicalProfile"
            erosions_data.user = request.user
            erosions_data.save()
            hypertension_data = hypertension_form.save(commit=False)
            hypertension_data.last_modified = "MedicalProfile"
            hypertension_data.user = request.user
            hypertension_data.save()
            hyperuricemia_data = hyperuricemia_form.save(commit=False)
            hyperuricemia_data.last_modified = "MedicalProfile"
            hyperuricemia_data.user = request.user
            hyperuricemia_data.save()
            organ_transplant_data = organ_transplant_form.save(commit=False)
            organ_transplant_data.last_modified = "MedicalProfile"
            organ_transplant_data.user = request.user
            organ_transplant_data.save()
            urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
            urate_kidney_stones_data.last_modified = "MedicalProfile"
            urate_kidney_stones_data.user = request.user
            urate_kidney_stones_data.save()
            tophi_data = tophi_form.save(commit=False)
            tophi_data.last_modified = "MedicalProfile"
            tophi_data.user = request.user
            tophi_data.save()
            medical_profile_data.CKD = CKD_data
            medical_profile_data.hypertension = hypertension_data
            medical_profile_data.CHF = CHF_data
            medical_profile_data.diabetes = diabetes_data
            medical_profile_data.organ_transplant = organ_transplant_data
            medical_profile_data.urate_kidney_stones = urate_kidney_stones_data
            medical_profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    CHF_form=CHF_form,
                    CKD_form=CKD_form,
                    diabetes_form=diabetes_form,
                    erosions_form=erosions_form,
                    hypertension_form=hypertension_form,
                    hyperuricemia_form=hyperuricemia_form,
                    organ_transplant_form=organ_transplant_form,
                    urate_kidney_stones_form=urate_kidney_stones_form,
                    tophi_form=tophi_form,
                )
            )


class MedicalProfileUpdate(LoginRequiredMixin, UserDetailRedirectMixin, UpdateView):
    model = MedicalProfile
    form_class = MedicalProfileForm
    CKD_form_class = CKDForm
    hypertension_form_class = HypertensionForm
    hyperuricemia_form_class = HyperuricemiaForm
    CHF_form_class = CHFForm
    diabetes_form_class = DiabetesForm
    erosions_form_class = ErosionsForm
    organ_transplant_form_class = OrganTransplantForm
    urate_kidney_stone_form_class = UrateKidneyStonesForm
    tophi_form_class = TophiForm

    def get_context_data(self, **kwargs):
        context = super(MedicalProfileUpdate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        # Adds related model forms to context for rendering
        if self.request.POST:
            context["CHF_form"] = CHFForm(self.request.POST, instance=self.object.CHF)
            context["CKD_form"] = CKDForm(self.request.POST, instance=self.object.CKD)
            context["diabetes_form"] = DiabetesForm(self.request.POST, instance=self.object.diabetes)
            context["erosions_form"] = ErosionsForm(self.request.POST, instance=self.object.erosions)
            context["hypertension_form"] = HypertensionForm(self.request.POST, instance=self.object.hypertension)
            context["hyperuricemia_form"] = HyperuricemiaForm(self.request.POST, instance=self.object.hyperuricemia)
            context["organ_transplant_form"] = OrganTransplantForm(
                self.request.POST, instance=self.object.organ_transplant
            )
            context["urate_kidney_stones_form"] = UrateKidneyStonesForm(
                self.request.POST, instance=self.object.urate_kidney_stones
            )
            context["tophi_form"] = TophiForm(self.request.POST, instance=self.object.tophi)
        else:
            context["CKD_form"] = self.CKD_form_class(instance=self.object.CKD)
            context["CHF_form"] = self.CHF_form_class(instance=self.object.CHF)
            context["diabetes_form"] = self.diabetes_form_class(instance=self.object.diabetes)
            context["erosions_form"] = self.erosions_form_class(instance=self.object.erosions)
            context["hypertension_form"] = self.hypertension_form_class(instance=self.object.hypertension)
            context["hyperuricemia_form"] = self.hyperuricemia_form_class(instance=self.object.hyperuricemia)
            context["organ_transplant_form"] = self.organ_transplant_form_class(instance=self.object.organ_transplant)
            context["urate_kidney_stones_form"] = self.urate_kidney_stone_form_class(
                instance=self.object.urate_kidney_stones
            )
            context["tophi_form"] = self.tophi_form_class(instance=self.object.tophi)
        return context

    def get_object(self, queryset=None):
        try:
            queryset = self.model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(MedicalProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        # NEED **kwargs even though VSCode IDE says it's not used. Can't accept <user> and <pk> from url parameter otherwise.
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        CKD_form = self.CKD_form_class(request.POST, instance=self.object.CKD)
        CHF_form = self.CHF_form_class(request.POST, instance=self.object.CHF)
        diabetes_form = self.diabetes_form_class(request.POST, instance=self.object.diabetes)
        erosions_form = self.erosions_form_class(request.POST, instance=self.object.erosions)
        hypertension_form = self.hypertension_form_class(request.POST, instance=self.object.hypertension)
        hyperuricemia_form = self.hyperuricemia_form_class(request.POST, instance=self.object.hyperuricemia)
        organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=self.object.organ_transplant)
        urate_kidney_stones_form = self.urate_kidney_stone_form_class(
            request.POST, instance=self.object.urate_kidney_stones
        )
        tophi_form = self.tophi_form_class(request.POST, instance=self.object.tophi)

        if (
            form.is_valid()
            and CKD_form.is_valid()
            and CHF_form.is_valid()
            and diabetes_form.is_valid()
            and erosions_form.is_valid()
            and hypertension_form.is_valid()
            and hyperuricemia_form.is_valid()
            and organ_transplant_form.is_valid()
            and urate_kidney_stones_form.is_valid()
            and tophi_form.is_valid()
        ):
            medical_profile_data = form.save(commit=False)
            CHF_data = CHF_form.save(commit=False)
            CHF_data.last_modified = "MedicalProfile"
            CHF_data.save()
            CKD_data = CKD_form.save(commit=False)
            CKD_data.last_modified = "MedicalProfile"
            CKD_data.save()
            diabetes_data = diabetes_form.save(commit=False)
            diabetes_data.last_modified = "MedicalProfile"
            diabetes_data.save()
            erosions_data = erosions_form.save(commit=False)
            erosions_data.last_modified = "MedicalProfile"
            erosions_data.save()
            hypertension_data = hypertension_form.save(commit=False)
            hypertension_data.last_modified = "MedicalProfile"
            hypertension_data.save()
            hyperuricemia_data = hyperuricemia_form.save(commit=False)
            hyperuricemia_data.last_modified = "MedicalProfile"
            hyperuricemia_data.save()
            organ_transplant_data = organ_transplant_form.save(commit=False)
            organ_transplant_data.last_modified = "MedicalProfile"
            organ_transplant_data.save()
            urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
            urate_kidney_stones_data.last_modified = "MedicalProfile"
            urate_kidney_stones_data.save()
            tophi_data = tophi_form.save(commit=False)
            tophi_data.last_modified = "MedicalProfile"
            tophi_data.save()
            medical_profile_data.ckd = CKD_data
            medical_profile_data.CHF = CHF_data
            medical_profile_data.diabetes = diabetes_data
            medical_profile_data.erosions = erosions_data
            medical_profile_data.hypertension = hypertension_data
            medical_profile_data.hyperuricemia = hyperuricemia_data
            medical_profile_data.organ_transplant = organ_transplant_data
            medical_profile_data.urate_kidney_stones = urate_kidney_stones_data
            medical_profile_data.tophi = tophi_data
            medical_profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    CKD_form=CKD_form,
                    CHF_form=CHF_form,
                    diabetes_form=diabetes_form,
                    erosions_form=erosions_form,
                    hypertension_form=hypertension_form,
                    hyperuricemia_form=hypertension_form,
                    organ_transplant_form=organ_transplant_form,
                    urate_kidney_stones_form=urate_kidney_stones_form,
                    tophi_form=tophi_form,
                )
            )


class PatientProfileCreate(LoginRequiredMixin, UserDetailRedirectMixin, CreateView):
    model = PatientProfile
    form_class = PatientProfileForm
    height_form_class = HeightForm
    weight_form_class = WeightForm

    def get_context_data(self, **kwargs):
        context = super(PatientProfileCreate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if "height_form" not in context:
            context["height_form"] = self.height_form_class(self.request.GET)
        if "weight_form" not in context:
            context["weight_form"] = self.weight_form_class(self.request.GET)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=PatientProfile())
        height_form = self.height_form_class(request.POST, instance=Height())
        weight_form = self.weight_form_class(request.POST, instance=Weight())

        if form.is_valid() and height_form.is_valid() and weight_form.is_valid():
            profile_data = form.save(commit=False)
            profile_data.user = request.user
            height_data = height_form.save(commit=False)
            height_data.user = request.user
            height_data.save()
            weight_data = weight_form.save(commit=False)
            weight_data.user = request.user
            weight_data.save()
            profile_data.height = height_data
            profile_data.weight = weight_data
            profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, height_form=height_form, weight_form=weight_form)
            )


class PatientProfileUpdate(LoginRequiredMixin, UserDetailRedirectMixin, UpdateView):
    model = PatientProfile
    form_class = PatientProfileForm
    height_form_class = HeightForm
    weight_form_class = WeightForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PatientProfileUpdate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if self.request.POST:
            context["height_form"] = HeightForm(self.request.POST, instance=self.object.height)
            context["weight_form"] = WeightForm(self.request.POST, instance=self.object.weight)
        else:
            context["height_form"] = self.height_form_class(instance=self.object.height)
            context["weight_form"] = self.weight_form_class(instance=self.object.weight)
        return context

    def get_object(self, queryset=None):
        try:
            queryset = self.model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(PatientProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        # NEED **kwargs even though VSCode IDE says it's not used. Can't accept <user> and <pk> from url parameter otherwise.
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        height_form = self.height_form_class(request.POST, instance=self.object.height)
        weight_form = self.weight_form_class(request.POST, instance=self.object.weight)

        if form.is_valid() and height_form.is_valid() and weight_form.is_valid():
            profile_data = form.save(commit=False)
            if "value" in height_form.changed_data:
                height_data = height_form.save(commit=False)
                height_data.pk = None
                height_data.save()
                weight_data = weight_form.save()
            elif "value" in weight_form.changed_data:
                height_data = height_form.save()
                weight_data = weight_form.save(commit=False)
                weight_data.pk = None
                weight_data.save()
            elif "value" in height_form.changed_data and "value" in weight_form.changed_data:
                height_data = height_form.save(commit=False)
                height_data.pk = None
                height_data.save()
                weight_data = weight_form.save(commit=False)
                weight_data.pk = None
                weight_data.save()
            else:
                ### WHY NOT SAVE THESE FORMS OUTRIGHT??? ###
                height_data = height_form.save(commit=False)
                height_data.save()
                weight_data = weight_form.save(commit=False)
                weight_data.save()
            profile_data.height = height_data
            profile_data.weight = weight_data
            profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, height_form=height_form, weight_form=weight_form)
            )


class SocialProfileCreate(LoginRequiredMixin, AssignUserMixin, UserDetailRedirectMixin, CreateView):
    model = SocialProfile
    form_class = SocialProfileForm
    alcohol_form_class = AlcoholForm
    fructose_form_class = FructoseForm
    shellfish_form_class = ShellfishForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SocialProfileCreate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if "alcohol_form" not in context:
            context["alcohol_form"] = self.alcohol_form_class(self.request.GET)
        if "fructose_form" not in context:
            context["fructose_form"] = self.fructose_form_class(self.request.GET)
        if "shellfish_form" not in context:
            context["shellfish_form"] = self.shellfish_form_class(self.request.GET)
        return context

    def get_object(self, queryset=None):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=SocialProfile())
        alcohol_form = self.alcohol_form_class(request.POST, instance=Alcohol())
        fructose_form = self.fructose_form_class(request.POST, instance=Fructose())
        shellfish_form = self.shellfish_form_class(request.POST, instance=Shellfish())

        if form.is_valid() and alcohol_form.is_valid() and fructose_form.is_valid() and shellfish_form.is_valid():
            social_profile_data = form.save(commit=False)
            social_profile_data.user = request.user
            alcohol_data = alcohol_form.save(commit=False)
            alcohol_data.user = request.user
            alcohol_data.save()
            fructose_data = fructose_form.save(commit=False)
            fructose_data.user = request.user
            fructose_data.save()
            shellfish_data = shellfish_form.save(commit=False)
            shellfish_data.user = request.user
            shellfish_data.save()
            social_profile_data.stroke = alcohol_data
            social_profile_data.heartattack = fructose_data
            social_profile_data.bleed = shellfish_data
            social_profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    alcohol_form=alcohol_form,
                    fructose_form=fructose_form,
                    shellfish_form=shellfish_form,
                )
            )


class SocialProfileUpdate(LoginRequiredMixin, AssignUserMixin, UserDetailRedirectMixin, UpdateView):
    model = SocialProfile
    form_class = SocialProfileForm
    alcohol_form_class = AlcoholForm
    fructose_form_class = FructoseForm
    shellfish_form_class = ShellfishForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SocialProfileUpdate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if self.request.POST:
            context["alcohol_form"] = AlcoholForm(self.request.POST, instance=self.object.alcohol)
            context["fructose_form"] = FructoseForm(self.request.POST, instance=self.object.fructose)
            context["shellfish_form"] = ShellfishForm(self.request.POST, instance=self.object.shellfish)
        else:
            context["alcohol_form"] = self.alcohol_form_class(instance=self.object.alcohol)
            context["fructose_form"] = self.fructose_form_class(instance=self.object.fructose)
            context["shellfish_form"] = self.shellfish_form_class(instance=self.object.shellfish)
        return context

    def get_object(self, queryset=None):
        try:
            queryset = self.model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(SocialProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        # NEED **kwargs even though VSCode IDE says it's not used. Can't accept <user> and <pk> from url parameter otherwise.
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        alcohol_form = self.alcohol_form_class(request.POST, instance=self.object.alcohol)
        fructose_form = self.fructose_form_class(request.POST, instance=self.object.fructose)
        shellfish_form = self.shellfish_form_class(request.POST, instance=self.object.shellfish)

        if form.is_valid() and alcohol_form.is_valid() and fructose_form.is_valid() and shellfish_form.is_valid():
            social_profile_data = form.save(commit=False)
            alcohol_data = alcohol_form.save()
            fructose_data = fructose_form.save()
            shellfish_data = shellfish_form.save()
            social_profile_data.alcohol = alcohol_data
            social_profile_data.fructose = fructose_data
            social_profile_data.shellfish = shellfish_data
            social_profile_data.save()
            return HttpResponseRedirect(self.request.user.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    alcohol_form=alcohol_form,
                    fructose_form=fructose_form,
                    shellfish_form=shellfish_form,
                )
            )
