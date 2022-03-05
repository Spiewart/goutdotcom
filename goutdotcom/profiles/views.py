from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.urls import reverse
from django.views.generic import UpdateView

from ..history.forms import (
    AlcoholForm,
    AnemiaForm,
    AnginaForm,
    AnticoagulationSimpleForm,
    BleedSimpleForm,
    CHFForm,
    CKDForm,
    ColchicineInteractionsForm,
    DiabetesSimpleForm,
    ErosionsForm,
    FructoseForm,
    GoutForm,
    HeartAttackSimpleForm,
    HypertensionForm,
    HyperuricemiaForm,
    IBDForm,
    LeukocytosisForm,
    LeukopeniaForm,
    OrganTransplantForm,
    OsteoporosisForm,
    PolycythemiaForm,
    ShellfishForm,
    StrokeSimpleForm,
    ThrombocytopeniaForm,
    ThrombocytosisForm,
    TophiForm,
    TransaminitisForm,
    UrateKidneyStonesForm,
)
from ..lab.forms import (
    BaselineALTForm,
    BaselineASTForm,
    BaselineCreatinineForm,
    BaselineHemoglobinForm,
    BaselinePlateletForm,
    BaselineWBCForm,
)
from ..utils.mixins import PatientProviderMixin
from ..vitals.forms import HeightForm, WeightForm
from .forms import (
    FamilyProfileForm,
    MedicalProfileForm,
    PatientProfileForm,
    ProviderProfileForm,
    SocialProfileForm,
)
from .models import (
    FamilyProfile,
    MedicalProfile,
    PatientProfile,
    ProviderProfile,
    SocialProfile,
)


# Mixins
class UserDetailRedirectMixin:
    # Mixin to check if the logged in User is a Patient, redirect to his/her own UserDetail page if so
    # If logged in User is Provider, redirect to Patient UserDetail page
    # Else redirect to home ### NEED TO SWITCH TO ERROR REDIRECT INF UTURE
    def get_success_url(self):
        if self.request.user.role == "PATIENT":
            return self.request.user.get_absolute_url()
        elif self.request.user.role == "PROVIDER":
            return self.object.user.get_absolute_url()
        else:
            return HttpResponseRedirect(reverse("/"))


class FamilyProfileUpdate(LoginRequiredMixin, PatientProviderMixin, UserDetailRedirectMixin, UpdateView):
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


class MedicalProfileUpdate(LoginRequiredMixin, PatientProviderMixin, UserDetailRedirectMixin, UpdateView):
    model = MedicalProfile
    form_class = MedicalProfileForm
    alt_form_class = BaselineALTForm
    ast_form_class = BaselineASTForm
    anemia_form_class = AnemiaForm
    angina_form_class = AnginaForm
    anticoagulation_form_class = AnticoagulationSimpleForm
    bleed_form_class = BleedSimpleForm
    CHF_form_class = CHFForm
    CKD_form_class = CKDForm
    colchicine_interactions_form_class = ColchicineInteractionsForm
    creatinine_form_class = BaselineCreatinineForm
    diabetes_form_class = DiabetesSimpleForm
    erosions_form_class = ErosionsForm
    heartattack_form_class = HeartAttackSimpleForm
    hemoglobin_form_class = BaselineHemoglobinForm
    hypertension_form_class = HypertensionForm
    hyperuricemia_form_class = HyperuricemiaForm
    IBD_form_class = IBDForm
    leukocytosis_form_class = LeukocytosisForm
    leukopenia_form_class = LeukopeniaForm
    organ_transplant_form_class = OrganTransplantForm
    osteoporosis_form_class = OsteoporosisForm
    platelet_form_class = BaselinePlateletForm
    polycythemia_form_class = PolycythemiaForm
    stroke_form_class = StrokeSimpleForm
    thrombocytopenia_form_class = ThrombocytopeniaForm
    thrombocytosis_form_class = ThrombocytosisForm
    tophi_form_class = TophiForm
    transaminitis_form_class = TransaminitisForm
    urate_kidney_stone_form_class = UrateKidneyStonesForm
    wbc_form_class = BaselineWBCForm

    def get_context_data(self, **kwargs):
        context = super(MedicalProfileUpdate, self).get_context_data(**kwargs)
        # Adds related model forms to context for rendering
        if self.request.POST:
            context["alt_form"] = self.alt_form_class(
                self.request.POST, instance=self.object.transaminitis.baseline_alt, prefix="alt_transaminitis"
            )
            context["anemia_form"] = self.anemia_form_class(self.request.POST, instance=self.object.anemia)
            context["angina_form"] = self.angina_form_class(self.request.POST, instance=self.object.angina)
            context["anticoagulation_form"] = self.anticoagulation_form_class(
                self.request.POST, instance=self.object.anticoagulation
            )
            context["ast_form"] = self.ast_form_class(
                self.request.POST, instance=self.object.transaminitis.baseline_ast, prefix="ast_transaminitis"
            )
            context["bleed_form"] = self.bleed_form_class(self.request.POST, instance=self.object.bleed)
            context["CHF_form"] = self.CHF_form_class(self.request.POST, instance=self.object.CHF)
            context["CKD_form"] = self.CKD_form_class(self.request.POST, instance=self.object.CKD)
            context["creatinine_form"] = self.creatinine_form_class(
                self.request.POST, instance=self.object.CKD.baseline, prefix="creatinine_CKD"
            )
            context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                self.request.POST, instance=self.object.colchicine_interactions
            )
            context["diabetes_form"] = self.diabetes_form_class(self.request.POST, instance=self.object.diabetes)
            context["erosions_form"] = self.erosions_form_class(self.request.POST, instance=self.object.erosions)
            context["heartattack_form"] = self.heartattack_form_class(
                self.request.POST, instance=self.object.heartattack
            )
            context["hemoglobin_polycythemia_form"] = self.hemoglobin_form_class(
                self.request.POST, instance=self.object.polycythemia.baseline, prefix="hemoglobin_polycythemia"
            )
            context["hemoglobin_anemia_form"] = self.hemoglobin_form_class(
                self.request.POST, instance=self.object.anemia.baseline, prefix="hemoglobin_anemia"
            )
            context["hypertension_form"] = self.hypertension_form_class(
                self.request.POST, instance=self.object.hypertension
            )
            context["hyperuricemia_form"] = self.hyperuricemia_form_class(
                self.request.POST, instance=self.object.hyperuricemia
            )
            context["IBD_form"] = self.IBD_form_class(self.request.POST, instance=self.object.IBD)
            context["leukocytosis_form"] = self.leukocytosis_form_class(
                self.request.POST, instance=self.object.leukocytosis
            )
            context["leukopenia_form"] = self.leukopenia_form_class(self.request.POST, instance=self.object.leukopenia)
            context["organ_transplant_form"] = self.organ_transplant_form_class(
                self.request.POST, instance=self.object.organ_transplant
            )
            context["osteoporosis_form"] = self.osteoporosis_form_class(
                self.request.POST, instance=self.object.osteoporosis
            )
            context["platelet_thrombocytosis_form"] = self.platelet_form_class(
                self.request.POST, instance=self.object.thrombocytosis.baseline, prefix="platelet_thrombocytosis"
            )
            context["platelet_thrombocytopenia_form"] = self.platelet_form_class(
                self.request.POST, instance=self.object.thrombocytopenia.baseline, prefix="platelet_thrombocytopenia"
            )
            context["polycythemia_form"] = self.polycythemia_form_class(
                self.request.POST, instance=self.object.polycythemia
            )
            context["stroke_form"] = self.stroke_form_class(self.request.POST, instance=self.object.stroke)
            context["urate_kidney_stones_form"] = self.urate_kidney_stone_form_class(
                self.request.POST, instance=self.object.urate_kidney_stones
            )
            context["tophi_form"] = self.tophi_form_class(self.request.POST, instance=self.object.tophi)
            context["thrombocytosis_form"] = self.thrombocytopenia_form_class(
                self.request.POST, instance=self.object.thrombocytosis
            )
            context["thrombocytopenia_form"] = self.thrombocytopenia_form_class(
                self.request.POST, instance=self.object.thrombocytopenia
            )
            context["transaminitis_form"] = self.transaminitis_form_class(
                self.request.POST, instance=self.object.transaminitis
            )
            context["wbc_leukocytosis_form"] = self.wbc_form_class(
                self.request.POST, instance=self.object.leukocytosis.baseline, prefix="wbc_leukocytosis"
            )
            context["wbc_leukoepenia_form"] = self.wbc_form_class(
                self.request.POST, instance=self.object.leukopenia.baseline, prefix="wbc_leukopenia"
            )
        else:
            context["alt_form"] = self.alt_form_class(
                instance=self.object.transaminitis.baseline_alt, prefix="alt_transaminitis"
            )
            context["anemia_form"] = self.anemia_form_class(instance=self.object.anemia)
            context["angina_form"] = self.angina_form_class(instance=self.object.angina)
            context["anticoagulation_form"] = self.anticoagulation_form_class(instance=self.object.anticoagulation)
            context["ast_form"] = self.ast_form_class(
                instance=self.object.transaminitis.baseline_ast, prefix="ast_transaminitis"
            )
            context["bleed_form"] = self.bleed_form_class(instance=self.object.bleed)
            context["CKD_form"] = self.CKD_form_class(instance=self.object.CKD)
            context["CHF_form"] = self.CHF_form_class(instance=self.object.CHF)
            context["colchicine_interactions_form"] = self.colchicine_interactions_form_class(
                instance=self.object.colchicine_interactions
            )
            context["creatinine_form"] = self.creatinine_form_class(
                instance=self.object.CKD.baseline, prefix="creatinine_CKD"
            )
            context["diabetes_form"] = self.diabetes_form_class(instance=self.object.diabetes)
            context["erosions_form"] = self.erosions_form_class(instance=self.object.erosions)
            context["heartattack_form"] = self.heartattack_form_class(instance=self.object.heartattack)
            context["hemoglobin_polycythemia_form"] = self.hemoglobin_form_class(
                instance=self.object.polycythemia.baseline, prefix="hemoglobin_polycythemia"
            )
            context["hemoglobin_anemia_form"] = self.hemoglobin_form_class(
                instance=self.object.anemia.baseline, prefix="hemoglobin_anemia"
            )
            context["hypertension_form"] = self.hypertension_form_class(instance=self.object.hypertension)
            context["hyperuricemia_form"] = self.hyperuricemia_form_class(instance=self.object.hyperuricemia)
            context["IBD_form"] = self.IBD_form_class(instance=self.object.IBD)
            context["leukocytosis_form"] = self.leukocytosis_form_class(instance=self.object.leukocytosis)
            context["leukopenia_form"] = self.leukopenia_form_class(instance=self.object.leukopenia)
            context["organ_transplant_form"] = self.organ_transplant_form_class(instance=self.object.organ_transplant)
            context["osteoporosis_form"] = self.osteoporosis_form_class(instance=self.object.osteoporosis)
            context["platelet_thrombocytosis_form"] = self.platelet_form_class(
                instance=self.object.thrombocytosis.baseline, prefix="platelet_thrombocytosis"
            )
            context["platelet_thrombocytopenia_form"] = self.platelet_form_class(
                instance=self.object.thrombocytopenia.baseline, prefix="platelet_thrombocytopenia"
            )
            context["polycythemia_form"] = self.polycythemia_form_class(instance=self.object.polycythemia)
            context["stroke_form"] = self.stroke_form_class(instance=self.object.stroke)
            context["tophi_form"] = self.tophi_form_class(instance=self.object.tophi)
            context["thrombocytopenia_form"] = self.thrombocytopenia_form_class(instance=self.object.thrombocytopenia)
            context["thrombocytosis_form"] = self.thrombocytosis_form_class(instance=self.object.thrombocytosis)
            context["transaminitis_form"] = self.transaminitis_form_class(instance=self.object.transaminitis)
            context["urate_kidney_stones_form"] = self.urate_kidney_stone_form_class(
                instance=self.object.urate_kidney_stones
            )
            context["wbc_leukocytosis_form"] = self.wbc_form_class(
                instance=self.object.leukocytosis.baseline, prefix="wbc_leukocytosis"
            )
            context["wbc_leukopenia_form"] = self.wbc_form_class(
                instance=self.object.leukopenia.baseline, prefix="wbc_leukopenia"
            )
        return context

    def get_object(self, queryset=None):
        try:
            # Get MedicalProfile from pk in **kwargs
            queryset = self.model.objects.filter(slug=self.kwargs["slug"])
        except ObjectDoesNotExist:
            # Else return 404
            raise Http404("No object found matching this query.")
        obj = super(MedicalProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        ## NEED **kwargs even though VSCode IDE says it's not used. Can't accept <user> and <pk> from url parameter otherwise.
        # Fetches instance of MedicalProfile model and associated OnetoOne related models for UpdateView
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        alt_form = self.alt_form_class(
            request.POST, instance=self.object.transaminitis.baseline_alt, prefix="alt_transaminitis"
        )
        anemia_form = self.anemia_form_class(request.POST, instance=self.object.anemia)
        angina_form = self.angina_form_class(request.POST, instance=self.object.angina)
        anticoagulation_form = self.anticoagulation_form_class(request.POST, instance=self.object.anticoagulation)
        ast_form = self.ast_form_class(
            request.POST, instance=self.object.transaminitis.baseline_ast, prefix="ast_transaminitis"
        )
        bleed_form = self.bleed_form_class(request.POST, instance=self.object.bleed)
        CKD_form = self.CKD_form_class(request.POST, instance=self.object.CKD)
        CHF_form = self.CHF_form_class(request.POST, instance=self.object.CHF)
        colchicine_interactions_form = self.colchicine_interactions_form_class(
            request.POST, instance=self.object.colchicine_interactions
        )
        creatinine_form = self.creatinine_form_class(
            request.POST, instance=self.object.CKD.baseline, prefix="creatinine_CKD"
        )
        diabetes_form = self.diabetes_form_class(request.POST, instance=self.object.diabetes)
        erosions_form = self.erosions_form_class(request.POST, instance=self.object.erosions)
        heartattack_form = self.heartattack_form_class(request.POST, instance=self.object.heartattack)
        hemoglobin_anemia_form = self.hemoglobin_form_class(
            request.POST, instance=self.object.anemia.baseline, prefix="hemoglobin_anemia"
        )
        hemoglobin_polycythemia_form = self.hemoglobin_form_class(
            request.POST, instance=self.object.polycythemia.baseline, prefix="hemoglobin_polycythemia"
        )
        hypertension_form = self.hypertension_form_class(request.POST, instance=self.object.hypertension)
        hyperuricemia_form = self.hyperuricemia_form_class(request.POST, instance=self.object.hyperuricemia)
        IBD_form = self.IBD_form_class(request.POST, instance=self.object.IBD)
        leukocytosis_form = self.leukocytosis_form_class(request.POST, instance=self.object.leukocytosis)
        leukopenia_form = self.leukopenia_form_class(request.POST, instance=self.object.leukopenia)
        organ_transplant_form = self.organ_transplant_form_class(request.POST, instance=self.object.organ_transplant)
        osteoporosis_form = self.osteoporosis_form_class(request.POST, instance=self.object.osteoporosis)
        platelet_thrombocytosis_form = self.platelet_form_class(
            request.POST, instance=self.object.thrombocytosis.baseline, prefix="platelet_thrombocytosis"
        )
        platelet_thrombocytopenia_form = self.platelet_form_class(
            request.POST, instance=self.object.thrombocytopenia.baseline, prefix="platelet_thrombocytopenia"
        )
        polycythemia_form = self.polycythemia_form_class(request.POST, instance=self.object.polycythemia)
        stroke_form = self.stroke_form_class(request.POST, instance=self.object.stroke)
        thrombocytosis_form = self.thrombocytosis_form_class(request.POST, instance=self.object.thrombocytosis)
        thrombocytopenia_form = self.thrombocytopenia_form_class(request.POST, instance=self.object.thrombocytopenia)
        tophi_form = self.tophi_form_class(request.POST, instance=self.object.tophi)
        transaminitis_form = self.transaminitis_form_class(request.POST, instance=self.object.transaminitis)
        urate_kidney_stones_form = self.urate_kidney_stone_form_class(
            request.POST, instance=self.object.urate_kidney_stones
        )
        wbc_leukocytosis_form = self.wbc_form_class(
            request.POST, instance=self.object.leukocytosis.baseline, prefix="wbc_leukocytosis"
        )
        wbc_leukopenia_form = self.wbc_form_class(
            request.POST, instance=self.object.leukopenia.baseline, prefix="wbc_leukopenia"
        )

        if (
            form.is_valid()
            and alt_form.is_valid()
            and anemia_form.is_valid()
            and angina_form.is_valid()
            and anticoagulation_form.is_valid()
            and ast_form.is_valid()
            and bleed_form.is_valid()
            and CKD_form.is_valid()
            and CHF_form.is_valid()
            and colchicine_interactions_form.is_valid()
            and creatinine_form.is_valid()
            and diabetes_form.is_valid()
            and erosions_form.is_valid()
            and heartattack_form.is_valid()
            and hemoglobin_anemia_form.is_valid()
            and hemoglobin_polycythemia_form.is_valid()
            and hypertension_form.is_valid()
            and hyperuricemia_form.is_valid()
            and IBD_form.is_valid()
            and leukocytosis_form.is_valid()
            and leukopenia_form.is_valid()
            and organ_transplant_form.is_valid()
            and osteoporosis_form.is_valid()
            and polycythemia_form.is_valid()
            and platelet_thrombocytopenia_form.is_valid()
            and platelet_thrombocytosis_form.is_valid()
            and stroke_form.is_valid()
            and thrombocytosis_form.is_valid()
            and thrombocytopenia_form.is_valid()
            and transaminitis_form.is_valid()
            and tophi_form.is_valid()
            and urate_kidney_stones_form.is_valid()
            and wbc_leukocytosis_form.is_valid()
            and wbc_leukopenia_form.is_valid()
        ):
            # Check if forms are valid
            # Check if related models are changed in form.changed_data, if so process them, assign last_modified to MedicalProfile, save to MedicalProfile
            medical_profile_data = form.save(commit=False)
            anemia_data = anemia_form.save(commit=False)
            polycythemia_data = polycythemia_form.save(commit=False)
            CKD_data = CKD_form.save(commit=False)
            leukocytosis_data = leukocytosis_form.save(commit=False)
            leukopenia_data = leukopenia_form.save(commit=False)
            thrombocytopenia_data = thrombocytopenia_form.save(commit=False)
            thrombocytosis_data = thrombocytosis_form.save(commit=False)
            transaminitis_data = transaminitis_form.save(commit=False)
            if "value" in alt_form.changed_data:
                alt_data = alt_form.save(commit=False)
                alt_data.last_modified = "MedicalProfile"
                alt_data.user = self.object.user
                alt_data.save()
                transaminitis_data.baseline_alt = alt_data
            if "value" in ast_form.changed_data:
                transaminitis_data = transaminitis_form.save(commit=False)
                ast_data = ast_form.save(commit=False)
                ast_data.last_modified = "MedicalProfile"
                ast_data.user = self.object.user
                ast_data.save()
                transaminitis_data.baseline_ast = ast_data
            if (
                "value" in alt_form.changed_data
                or "value" in ast_form.changed_data
                or "value" in transaminitis_form.changed_data
            ):
                transaminitis_data.last_modified = "MedicalProfile"
                transaminitis_data.save()
                medical_profile_data.transaminitis = transaminitis_data
            if "value" in hemoglobin_anemia_form.changed_data:
                if hemoglobin_anemia_form.data["hemoglobin_anemia-value"]:
                    hemoglobin_anemia_data = hemoglobin_anemia_form.save(commit=False)
                    hemoglobin_anemia_data.last_modified = "MedicalProfile"
                    hemoglobin_anemia_data.user = self.object.user
                    hemoglobin_anemia_data.save()
                    anemia_data.baseline = hemoglobin_anemia_data
                else:
                    anemia_data.baseline = None
            if "value" in anemia_form.changed_data or "value" in hemoglobin_anemia_form.changed_data:
                anemia_data.last_modified = "MedicalProfile"
                anemia_data.save()
                medical_profile_data.anemia = anemia_data
            if "value" in anticoagulation_form.changed_data:
                anticoagulation_data = anticoagulation_form.save(commit=False)
                anticoagulation_data.last_modified = "MedicalProfile"
                anticoagulation_data.save()
                medical_profile_data.anticoagulation = anticoagulation_data
            if "value" in bleed_form.changed_data:
                bleed_data = bleed_form.save(commit=False)
                bleed_data.last_modified = "MedicalProfile"
                bleed_data.save()
                medical_profile_data.bleed = bleed_data
            if "value" in CHF_form.changed_data:
                CHF_data = CHF_form.save(commit=False)
                CHF_data.last_modified = "MedicalProfile"
                CHF_data.save()
                medical_profile_data.CHF = CHF_data
            if "value" in creatinine_form.changed_data:
                if creatinine_form.data["creatinine_CKD-value"]:
                    creatinine_data = creatinine_form.save(commit=False)
                    creatinine_data.last_modified = "MedicalProfile"
                    creatinine_data.user = self.object.user
                    creatinine_data.save()
                    CKD_data.baseline = creatinine_data
                else:
                    CKD_data.baseline == None
            if "value" in CKD_form.changed_data or "value" in creatinine_form.changed_data:
                CKD_data.last_modified = "MedicalProfile"
                CKD_data.save()
                medical_profile_data.CKD = CKD_data
            if "value" in colchicine_interactions_form.changed_data:
                colchicine_interactions_data = colchicine_interactions_form.save(commit=False)
                colchicine_interactions_data.last_modified = "MedicalProfile"
                colchicine_interactions_data.save()
                medical_profile_data.colchicine_interactions = colchicine_interactions_data
            if "value" in diabetes_form.changed_data:
                diabetes_data = diabetes_form.save(commit=False)
                diabetes_data.last_modified = "MedicalProfile"
                diabetes_data.save()
                medical_profile_data.diabetes = diabetes_data
            if "value" in erosions_form.changed_data:
                erosions_data = erosions_form.save(commit=False)
                erosions_data.last_modified = "MedicalProfile"
                erosions_data.save()
                medical_profile_data.erosions = erosions_data
            if "value" in heartattack_form.changed_data:
                heartattack_data = heartattack_form.save(commit=False)
                heartattack_data.last_modified = "MedicalProfile"
                heartattack_data.save()
                medical_profile_data.heartattack = heartattack_data
            if "value" in hypertension_form.changed_data:
                hypertension_data = hypertension_form.save(commit=False)
                hypertension_data.last_modified = "MedicalProfile"
                hypertension_data.save()
                medical_profile_data.hypertension = hypertension_data
            if "value" in hyperuricemia_form.changed_data:
                hyperuricemia_data = hyperuricemia_form.save(commit=False)
                hyperuricemia_data.last_modified = "MedicalProfile"
                hyperuricemia_data.save()
                medical_profile_data.hyperuricemia = hyperuricemia_data
            if "value" in IBD_form.changed_data:
                IBD_data = IBD_form.save(commit=False)
                IBD_data.last_modified = "MedicalProfile"
                IBD_data.save()
                medical_profile_data.IBD = IBD_data
            if "value" in wbc_leukocytosis_form.changed_data:
                if wbc_leukocytosis_form.data["wbc_leukocytosis-value"]:
                    wbc_leukocytosis_data = wbc_leukocytosis_form.save(commit=False)
                    wbc_leukocytosis_data.last_modified = "MedicalProfile"
                    wbc_leukocytosis_data.user = self.object.user
                    wbc_leukocytosis_data.save()
                    leukocytosis_data.baseline = wbc_leukocytosis_data
                else:
                    leukocytosis_data.baseline = None
            if "value" in leukocytosis_form.changed_data or "value" in wbc_leukocytosis_form.changed_data:
                leukocytosis_data.last_modified = "MedicalProfile"
                leukocytosis_data.save()
                medical_profile_data.leukocytosis = leukocytosis_data
            if "value" in wbc_leukopenia_form.changed_data:
                if wbc_leukopenia_form.data["wbc_leukopenia-value"]:
                    wbc_leukopenia_data = wbc_leukopenia_form.save(commit=False)
                    wbc_leukopenia_data.last_modified = "MedicalProfile"
                    wbc_leukopenia_data.user = self.object.user
                    wbc_leukopenia_data.save()
                    leukopenia_data.baseline = wbc_leukopenia_data
                else:
                    leukopenia_data.baselin = None
            if "value" in leukopenia_form.changed_data or "value" in wbc_leukopenia_form.changed_data:
                leukopenia_data.last_modified = "MedicalProfile"
                leukopenia_data.save()
                medical_profile_data.leukopenia = leukopenia_data
            if "value" in organ_transplant_form.changed_data:
                organ_transplant_data = organ_transplant_form.save(commit=False)
                organ_transplant_data.last_modified = "MedicalProfile"
                organ_transplant_data.save()
                medical_profile_data.organ_transplant = organ_transplant_data
            if "value" in osteoporosis_form.changed_data:
                osteoporosis_data = osteoporosis_form.save(commit=False)
                osteoporosis_data.last_modified = "MedicalProfile"
                osteoporosis_data.save()
                medical_profile_data.osteoporosis = osteoporosis_data
            if "value" in hemoglobin_polycythemia_form.changed_data:
                if hemoglobin_polycythemia_form.data["hemoglobin_polycythemia-value"]:
                    hemoglobin_polycythemia_data = hemoglobin_polycythemia_form.save(commit=False)
                    hemoglobin_polycythemia_data.last_modified = "MedicalProfile"
                    hemoglobin_polycythemia_data.user = self.object.user
                    hemoglobin_polycythemia_data.save()
                    polycythemia_data.baseline = hemoglobin_polycythemia_data
                else:
                    polycythemia_data.baseline = None
            if "value" in polycythemia_form.changed_data or "value" in hemoglobin_polycythemia_form.changed_data:
                polycythemia_data.last_modified = "MedicalProfile"
                polycythemia_data.save()
                medical_profile_data.polycythemia = polycythemia_data
            if "value" in stroke_form.changed_data:
                stroke_data = stroke_form.save(commit=False)
                stroke_data.last_modified = "MedicalProfile"
                stroke_data.save()
                medical_profile_data.stroke = stroke_data
            if "value" in platelet_thrombocytopenia_form.changed_data:
                if platelet_thrombocytopenia_form.data["platelet_thrombocytopenia-value"]:
                    platelet_thrombocytopenia_data = platelet_thrombocytopenia_form.save(commit=False)
                    platelet_thrombocytopenia_data.last_modified = "MedicalProfile"
                    platelet_thrombocytopenia_data.user = self.object.user
                    platelet_thrombocytopenia_data.save()
                    thrombocytopenia_data.baseline = platelet_thrombocytopenia_data
                else:
                    thrombocytopenia_data.baseline = None
            if "value" in thrombocytopenia_form.changed_data or "value" in platelet_thrombocytopenia_form.changed_data:
                thrombocytopenia_data.last_modified = "MedicalProfile"
                thrombocytopenia_data.save()
                medical_profile_data.thrombocytopenia = thrombocytopenia_data
            if "value" in platelet_thrombocytosis_form.changed_data:
                if platelet_thrombocytopenia_form.data["platelet_thrombocytosis-value"]:
                    platelet_thrombocytosis_data = platelet_thrombocytosis_form.save(commit=False)
                    platelet_thrombocytosis_data.last_modified = "MedicalProfile"
                    platelet_thrombocytosis_data.user = self.object.user
                    platelet_thrombocytosis_data.save()
                    thrombocytosis_data.baseline = platelet_thrombocytosis_data
                else:
                    thrombocytosis_data.baseline = None
            if "value" in thrombocytosis_form.changed_data or "value" in platelet_thrombocytosis_form.changed_data:
                thrombocytosis_data.last_modified = "MedicalProfile"
                thrombocytosis_data.save()
                medical_profile_data.thrombocytosis = thrombocytosis_data
            if "value" in tophi_form.changed_data:
                tophi_data = tophi_form.save(commit=False)
                tophi_data.last_modified = "MedicalProfile"
                tophi_data.save()
                medical_profile_data.tophi = tophi_data
            if "value" in urate_kidney_stones_form.changed_data:
                urate_kidney_stones_data = urate_kidney_stones_form.save(commit=False)
                urate_kidney_stones_data.last_modified = "MedicalProfile"
                urate_kidney_stones_data.save()
                medical_profile_data.urate_kidney_stones = urate_kidney_stones_data
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    alt_form=alt_form,
                    anemia_form=anemia_form,
                    angina_form=angina_form,
                    anticoagulation_form=anticoagulation_form,
                    ast_form=ast_form,
                    bleed_form=bleed_form,
                    CKD_form=CKD_form,
                    CHF_form=CHF_form,
                    colchicine_interactions_form=colchicine_interactions_form,
                    creatinine_form=creatinine_form,
                    diabetes_form=diabetes_form,
                    erosions_form=erosions_form,
                    heartattack_form=heartattack_form,
                    hemoglobin_anemia_form=hemoglobin_anemia_form,
                    hemoglobin_polycythemia_form=hemoglobin_polycythemia_form,
                    hypertension_form=hypertension_form,
                    hyperuricemia_form=hypertension_form,
                    IBD_form=IBD_form,
                    leukocytosis_form=leukocytosis_form,
                    leukopenia_form=leukopenia_form,
                    organ_transplant_form=organ_transplant_form,
                    osteoporosis_form=osteoporosis_form,
                    platelet_thrombocytopenia_form=platelet_thrombocytopenia_form,
                    platelet_thrombocytosis_form=platelet_thrombocytosis_form,
                    polycythemia_form=polycythemia_form,
                    stroke_form=stroke_form,
                    tophi_form=tophi_form,
                    thrombocytosis_form=thrombocytosis_form,
                    thrombocytopenia_form=thrombocytopenia_form,
                    transaminitis_form=transaminitis_form,
                    urate_kidney_stones_form=urate_kidney_stones_form,
                    wbc_leukocytosis_form=wbc_leukocytosis_form,
                    wbc_leukopenia_form=wbc_leukopenia_form,
                )
            )


class PatientProfileUpdate(LoginRequiredMixin, PatientProviderMixin, UserDetailRedirectMixin, UpdateView):
    """View for Updating PatientProfile.
    Set up to require a PatientProfile.pk kwarg
    Multiform view, including Height and Weight forms populated by already created objects.

    Raises:
        Http404: if PatientProfile not found matching kwarg User and kwarg pk

    Returns:
        [Http200]: success_url to UserDetail page
    """

    model = PatientProfile
    form_class = PatientProfileForm
    height_form_class = HeightForm
    weight_form_class = WeightForm

    def get_context_data(self, **kwargs):
        context = super(PatientProfileUpdate, self).get_context_data(**kwargs)
        # Add Height and Weight forms to context with previously created objects set as instance
        if self.request.POST:
            # With request.POST if request is POST
            context["height_form"] = HeightForm(self.request.POST, instance=self.object.height)
            context["weight_form"] = WeightForm(self.request.POST, instance=self.object.weight)
        else:
            context["height_form"] = HeightForm(instance=self.object.height)
            context["weight_form"] = WeightForm(instance=self.object.weight)
        return context

    def get_object(self, queryset=None):
        try:
            # Get PatientProfile from slug in **kwargs
            queryset = self.model.objects.filter(slug=self.kwargs["slug"])
        except ObjectDoesNotExist:
            # Else return 404
            raise Http404("No object found matching this query.")
        obj = super(PatientProfileUpdate, self).get_object(queryset=queryset)
        return obj

    def post(self, request, **kwargs):
        # NEED **kwargs even though VSCode IDE says it's not used. Can't accept <user> and <pk> from url parameter otherwise.
        # Get object, create forms for post() processing
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        height_form = self.height_form_class(request.POST, instance=self.object.height)
        weight_form = self.weight_form_class(request.POST, instance=self.object.weight)

        if form.is_valid() and height_form.is_valid() and weight_form.is_valid():
            profile_data = form.save(commit=False)
            height_data = height_form.save(commit=False)
            weight_data = weight_form.save(commit=False)
            # Check if Height or Weight or both changed, make pk=None if so such that the ORM creates a new model instance and iterates the pk
            if "value" in height_form.changed_data:
                height_data.pk = None
            if "value" in weight_form.changed_data:
                weight_data.pk = None
            # Set Height and Weight User fields to the PatientProfile User (needed if new instances were created)
            height_data.user = self.object.user
            height_data.save()
            weight_data.user = self.object.user
            weight_data.save()
            profile_data.height = height_data
            profile_data.weight = weight_data
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, height_form=height_form, weight_form=weight_form)
            )


class ProviderProfileUpdate(LoginRequiredMixin, UserDetailRedirectMixin, UserPassesTestMixin, UpdateView):
    model = ProviderProfile
    form_class = ProviderProfileForm

    # Check if User is the same as the Profile User, return 404 if not
    def test_func(self):
        return self.request.user == self.object.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SocialProfileUpdate(LoginRequiredMixin, PatientProviderMixin, UserDetailRedirectMixin, UpdateView):
    model = SocialProfile
    form_class = SocialProfileForm
    alcohol_form_class = AlcoholForm
    fructose_form_class = FructoseForm
    shellfish_form_class = ShellfishForm

    def get_context_data(self, **kwargs):
        context = super(SocialProfileUpdate, self).get_context_data(**kwargs)
        # Add related model forms to context for GET and POST
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
            # Get SocialProfile from pk in **kwargs
            queryset = self.model.objects.filter(user__username=self.kwargs["user"])
        except ObjectDoesNotExist:
            # Else return 404
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
            # If forms are valid, assign related models to SocialProfile and call form_valid() to save
            social_profile_data = form.save(commit=False)
            alcohol_data = alcohol_form.save()
            fructose_data = fructose_form.save()
            shellfish_data = shellfish_form.save()
            social_profile_data.alcohol = alcohol_data
            social_profile_data.fructose = fructose_data
            social_profile_data.shellfish = shellfish_data
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    alcohol_form=alcohol_form,
                    fructose_form=fructose_form,
                    shellfish_form=shellfish_form,
                )
            )
