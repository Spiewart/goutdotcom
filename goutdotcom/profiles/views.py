from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from goutdotcom.history.forms import (
    BleedForm,
    CHFForm,
    CKDForm,
    DiabetesForm,
    HeartAttackForm,
    HypertensionForm,
    OrganTransplantForm,
    StrokeForm,
    UrateKidneyStonesForm,
)
from goutdotcom.history.models import (
    CHF,
    CKD,
    Bleed,
    Diabetes,
    HeartAttack,
    Hypertension,
    OrganTransplant,
    Stroke,
    UrateKidneyStones,
)
from goutdotcom.profiles.forms import (
    ContraindicationsProfileForm,
    MedicalProfileForm,
    PatientProfileForm,
)
from goutdotcom.vitals.forms import HeightForm, WeightForm
from goutdotcom.vitals.models import Height, Weight

from .models import ContraindicationsProfile, MedicalProfile, PatientProfile


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
            )
        else:
            context["CKD_form"] = self.CKD_form_class(instance=self.object.CKD)
            context["hypertension_form"] = self.hypertension_form_class(instance=self.object.hypertension)
            context["CHF_form"] = self.CHF_form_class(instance=self.object.CHF)
            context["diabetes_form"] = self.diabetes_form_class(instance=self.object.diabetes)
            context["organ_transplant_form"] = self.organ_transplant_form_class(instance=self.object.organ_transplant)
            context["urate_kidney_stones_form"] = self.urate_kidney_stone_form_class(
                instance=self.object.urate_kidney_stones
            )
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
        hypertension_form = self.hypertension_form_class(request.POST, instance=self.object.hypertension)
        CHF_form = self.CHF_form_class(request.POST, instance=self.object.CHF)
        diabetes_form = self.diabetes_form_class(request.POST, instance=self.object.diabetes)
        organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=self.object.organ_transplant)
        urate_kidney_stones_form = self.urate_kidney_stone_form_class(
            request.POST, instance=self.object.urate_kidney_stones
        )

        if (
            form.is_valid()
            and CKD_form.is_valid()
            and hypertension_form.is_valid()
            and CHF_form.is_valid()
            and diabetes_form.is_valid()
            and organ_transplant_form.is_valid()
            and urate_kidney_stones_form.is_valid()
        ):
            medical_profile_data = form.save(commit=False)
            CKD_data = CKD_form.save()
            hypertension_data = hypertension_form.save()
            CHF_data = CHF_form.save()
            diabetes_data = diabetes_form.save()
            organ_transplant_data = organ_transplant_form.save()
            urate_kidney_stones_data = urate_kidney_stones_form.save()
            medical_profile_data.ckd = CKD_data
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
                    CKD_form=CKD_form,
                    hypertension_form=hypertension_form,
                    CHF_form=CHF_form,
                    diabetes_form=diabetes_form,
                    organ_transplant_form=organ_transplant_form,
                    urate_kidney_stones_form=urate_kidney_stones_form,
                )
            )


class MedicalProfileCreate(LoginRequiredMixin, AssignUserMixin, CreateView):
    model = MedicalProfile
    form_class = MedicalProfileForm
    CKD_form_class = CKDForm
    hypertension_form_class = HypertensionForm
    CHF_form_class = CHFForm
    diabetes_form_class = DiabetesForm
    organ_transplant_form_class = OrganTransplantForm
    urate_kidney_stone_form_class = UrateKidneyStonesForm

    def get_context_data(self, **kwargs):
        context = super(MedicalProfileCreate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if "CKD_form" not in context:
            context["CKD_form"] = self.CKD_form_class(self.request.GET)
        if "hypertension_form" not in context:
            context["hypertension_form"] = self.hypertension_form_class(self.request.GET)
        if "CHF_form" not in context:
            context["CHF_form"] = self.CHF_form_class(self.request.GET)
        if "diabetes_form" not in context:
            context["diabetes_form"] = self.diabetes_form_class(self.request.GET)
        if "organ_transplant_form" not in context:
            context["organ_transplant_form"] = self.organ_transplant_form_class(self.request.GET)
        if "urate_kidney_stones_form" not in context:
            context["urate_kidney_stones_form"] = self.urate_kidney_stone_form_class(self.request.GET)
        return context

    def get_object(self, queryset=None):
        object = self.model
        return object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=MedicalProfile())
        CKD_form = self.CKD_form_class(request.POST, instance=CKD())
        hypertension_form = self.hypertension_form_class(request.POST, instance=Hypertension())
        CHF_form = self.CHF_form_class(request.POST, instance=CHF())
        diabetes_form = self.diabetes_form_class(request.POST, instance=Diabetes())
        organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=OrganTransplant())
        urate_kidney_stones_form = self.urate_kidney_stone_form_class(request.POST, instance=UrateKidneyStones())

        if (
            form.is_valid()
            and CKD_form.is_valid()
            and hypertension_form.is_valid()
            and CHF_form.is_valid()
            and diabetes_form.is_valid()
            and organ_transplant_form.is_valid()
            and urate_kidney_stones_form.is_valid()
        ):
            medical_profile_data = form.save(commit=False)
            medical_profile_data.user = request.user
            CKD_data = CKD_form.save(commit=False)
            CKD_data.user = request.user
            CKD_data.save()
            hypertension_data = hypertension_form.save(commit=False)
            hypertension_data.user = request.user
            hypertension_data.save()
            CHF_data = CHF_form.save(commit=False)
            CHF_data.user = request.user
            CHF_data.save()
            diabetes_data = diabetes_form.save(commit=False)
            diabetes_data.user = request.user
            diabetes_data.save()
            organ_transplant_data = organ_transplant_form.save(commit=False)
            organ_transplant_data.user = request.user
            organ_transplant_data.save()
            urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
            urate_kidney_stones_data.user = request.user
            urate_kidney_stones_data.save()
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
                    CKD_form=CKD_form,
                    hypertension_form=hypertension_form,
                    CHF_form=CHF_form,
                    diabetes_form=diabetes_form,
                    organ_transplant_form=organ_transplant_form,
                    urate_kidney_stones_form=urate_kidney_stones_form,
                )
            )


class MedicalProfileUpdate(LoginRequiredMixin, UserDetailRedirectMixin, UpdateView):
    model = MedicalProfile
    form_class = MedicalProfileForm
    CKD_form_class = CKDForm
    hypertension_form_class = HypertensionForm
    CHF_form_class = CHFForm
    diabetes_form_class = DiabetesForm
    organ_transplant_form_class = OrganTransplantForm
    urate_kidney_stone_form_class = UrateKidneyStonesForm

    def get_context_data(self, **kwargs):
        context = super(MedicalProfileUpdate, self).get_context_data(**kwargs)
        context.update({"user": self.request.user})
        if self.request.POST:
            context["CKD_form"] = CKDForm(self.request.POST, instance=self.object.CKD)
            context["hypertension_form"] = HypertensionForm(self.request.POST, instance=self.object.hypertension)
            context["CHF_form"] = CHFForm(self.request.POST, instance=self.object.CHF)
            context["diabetes_form"] = DiabetesForm(self.request.POST, instance=self.object.diabetes)
            context["organ_transplant_form"] = OrganTransplantForm(
                self.request.POST, instance=self.object.organ_transplant
            )
            context["urate_kidney_stones_form"] = UrateKidneyStonesForm(
                self.request.POST, instance=self.object.urate_kidney_stones
            )
        else:
            context["CKD_form"] = self.CKD_form_class(instance=self.object.CKD)
            context["hypertension_form"] = self.hypertension_form_class(instance=self.object.hypertension)
            context["CHF_form"] = self.CHF_form_class(instance=self.object.CHF)
            context["diabetes_form"] = self.diabetes_form_class(instance=self.object.diabetes)
            context["organ_transplant_form"] = self.organ_transplant_form_class(instance=self.object.organ_transplant)
            context["urate_kidney_stones_form"] = self.urate_kidney_stone_form_class(
                instance=self.object.urate_kidney_stones
            )
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
        hypertension_form = self.hypertension_form_class(request.POST, instance=self.object.hypertension)
        CHF_form = self.CHF_form_class(request.POST, instance=self.object.CHF)
        diabetes_form = self.diabetes_form_class(request.POST, instance=self.object.diabetes)
        organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=self.object.organ_transplant)
        urate_kidney_stones_form = self.urate_kidney_stone_form_class(
            request.POST, instance=self.object.urate_kidney_stones
        )

        if (
            form.is_valid()
            and CKD_form.is_valid()
            and hypertension_form.is_valid()
            and CHF_form.is_valid()
            and diabetes_form.is_valid()
            and organ_transplant_form.is_valid()
            and urate_kidney_stones_form.is_valid()
        ):
            medical_profile_data = form.save(commit=False)
            CKD_data = CKD_form.save()
            hypertension_data = hypertension_form.save()
            CHF_data = CHF_form.save()
            diabetes_data = diabetes_form.save()
            organ_transplant_data = organ_transplant_form.save()
            urate_kidney_stones_data = urate_kidney_stones_form.save()
            medical_profile_data.ckd = CKD_data
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
                    CKD_form=CKD_form,
                    hypertension_form=hypertension_form,
                    CHF_form=CHF_form,
                    diabetes_form=diabetes_form,
                    organ_transplant_form=organ_transplant_form,
                    urate_kidney_stones_form=urate_kidney_stones_form,
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
