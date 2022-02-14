from datetime import datetime

from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, TemplateView, View

from ..lab.models import LabCheck
from ..ppxaid.models import PPxAid
from ..treatment.models import Colchicine, Prednisone
from ..ultaid.models import ULTAid
from ..utils.mixins import PatientProviderCreateMixin, PatientProviderMixin
from .models import ULTPlan

User = get_user_model()

# Create your views here.


class ULTPlanBluePrint(LoginRequiredMixin, PatientProviderMixin, TemplateView):
    template_name = "ultplan/blueprint.html"


class ULTPlanCreate(LoginRequiredMixin, PatientProviderCreateMixin, View):
    """View to pull data from User's PPxAid and ULTAid and create a ULTPlan without a form or any further User input.
    returns: ULTPlan instance"""

    def post(self, request, *args, **kwargs):
        self.username = self.kwargs.get("username")
        self.user = User.objects.get(username=self.username)
        # Checks if user has created a ULTAid, sets View ULTAid reference to None if not
        try:
            self.ultaid = ULTAid.objects.get(user=self.user)
        # Assigns user ULTAid to View ultaid if exists
        except ULTAid.DoesNotExist:
            self.ultaid = None
        # Checks if user has created a PPxAid, sets View ppxaid reference to None if not
        try:
            self.ppxaid = PPxAid.objects.get(user=self.user)
        # Assigns user PPxAid to View ppxaid if exists
        except PPxAid.DoesNotExist:
            self.ppxaid = None
        try:
            self.ultplan = ULTPlan.objects.get(user=self.user)
        except ULTPlan.DoesNotExist:
            self.ultplan = None
        if self.ultplan:
            return HttpResponseRedirect(reverse("ultplan:detail", kwargs={"slug": self.ultplan.slug}))
        # Checks if view ppxaid and ultaid are not None
        if self.ppxaid and self.ultaid:
            # Get ULT model from User's ULTAid decision_aid() 'drug' dict field
            ULT_model = apps.get_model("treatment", model_name=self.ultaid.decision_aid().get("drug"))
            # Get PPx model from User's PPxAid decision_aid() 'drug' dict field
            PPx_model = apps.get_model("treatment", model_name=self.ppxaid.decision_aid().get("drug"))
            # Create ULT instance from ULT_model and User's ULTAid decision_aid() 'dose' dict field
            ULT = ULT_model.objects.create(dose=self.ultaid.decision_aid().get("dose"), user=self.user)
            # Check if the PPx_model is Colchicine because the defaults for Colchicine need to be modified at object creation
            if PPx_model == Colchicine:
                PPx = PPx_model.objects.create(
                    dose=self.ppxaid.decision_aid().get("dose"),
                    freq=self.ppxaid.decision_aid().get("freq"),
                    dose2=None,
                    freq2=None,
                    dose3=None,
                    freq3=None,
                    prn=False,
                    as_prophylaxis=True,
                    user=self.user,
                    ppxaid=self.ppxaid,
                )
            elif PPx_model == Prednisone:
                PPx = PPx_model.objects.create(
                    dose=self.ppxaid.decision_aid().get("dose"),
                    freq=self.ppxaid.decision_aid().get("freq"),
                    dose2=None,
                    freq2=None,
                    duration2=None,
                    prn=False,
                    as_prophylaxis=True,
                    user=self.user,
                    ppxaid=self.ppxaid,
                )
            else:
                PPx = PPx_model.objects.create(
                    dose=self.ppxaid.decision_aid().get("dose"),
                    date_started=datetime.today(),
                    prn=False,
                    as_prophylaxis=True,
                    prophylaxis_finished=False,
                    user=self.user,
                    ppxaid=self.ppxaid,
                )
            # Create ULTPlan with the User, their ULTAid and PPxAid, ULTAid decision_aid() dict fields "dose", 'goal_urate' and 'titration_lab_interval'
            ultplan = ULTPlan.objects.create(
                user=self.user,
                creator=self.request.user,
                dose_adjustment=self.ultaid.decision_aid().get("dose"),
                goal_urate=self.ultaid.decision_aid().get("goal_urate"),
                titration_lab_interval=self.ultaid.decision_aid().get("titration_lab_interval"),
            )
            # After ultplan created, assign ULT.ultplan and PPx.ultplan to ultplan just created
            self.ultaid.ultplan = ultplan
            self.ultaid.save()
            ULT.ultplan = ultplan
            ULT.save()
            self.ppxaid.ultplan = ultplan
            self.ppxaid.save()
            PPx.ultplan = ultplan
            PPx.save()
            # Create initial LabCheck object for baseline labs
            LabCheck.objects.create(
                user=self.user,
                creator=self.request.user,
                ultplan=ultplan,
                due=datetime.today().date(),
            )

            # Return redirect to ultplan:detail
            messages.success(request, "ULTPlan created.")
            return HttpResponseRedirect(reverse("ultplan:detail", kwargs={"slug": ultplan.slug}))
        # These last 2 elif and else statements will only be called if a user types in the ultplan:create url rather than following the button-links displayed on their ULTAid detail page
        # If View ultaid exists but ppxaid does not, redirect to ppxaid:ultaid-create with kwargs user.ultaid.pk
        elif self.ultaid:
            return HttpResponseRedirect(
                reverse(
                    "ppxaid:user-ultaid-create",
                    kwargs={"ultaid": self.user.ultaid.slug, "username": self.user.username},
                )
            )
        # If neither ultaid nor ppxaid exists for view, redirect to ultaid:create to start the process
        else:
            return HttpResponseRedirect(reverse("ultaid:user-create", kwargs={"username": self.username}))


class ULTPlanDelete(LoginRequiredMixin, PatientProviderMixin, DeleteView):
    model = ULTPlan

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class ULTPlanDetail(LoginRequiredMixin, PatientProviderMixin, DetailView):
    model = ULTPlan


class ULTPlanUpdate(LoginRequiredMixin, PatientProviderMixin, View):
    """View to change a User's ULTPlan based on abnormal labs or reported medication side effects.
    returns: ULTPlan instance"""

    def post(self, request, *args, **kwargs):
        # Get User's ULTPlan
        try:
            self.ultplan = ULTPlan.objects.get(user=request.user)
        except ULTPlan.DoesNotExist:
            self.ultplan = None

        # Get ULTPlan's ULT and PPx
        self.ult = self.ultplan.get_ult()
        self.ppx = self.ultplan.get_ppx()

        # Attribute that will be used to tell the overall method whether to switch ULT or, in all other cases, to change the dosing
        switch = False

        if self.ult.intolerant == True:
            switch = True

        if self.ult._meta.model.__name__ == "Allopurinol":
            if self.ultplan.allopurinol.intolerant == True:
                pass
        elif self.ult._meta.model.__name__ == "Febuxostat":
            if self.ultplan.febuxostat.intolerant == True:
                pass
        else:
            pass
