from datetime import datetime

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, TemplateView, View

from ..ppxaid.models import PPxAid
from ..treatment.models import Colchicine, Prednisone
from ..ultaid.models import ULTAid
from .models import ULTPlan

# Create your views here.


class ULTPlanBluePrint(LoginRequiredMixin, TemplateView):
    template_name = "ultplan/blueprint.html"


class ULTPlanCreate(LoginRequiredMixin, View):
    """View to pull data from User's PPxAid and ULTAid and create a ULTPlan without a form or any further User input.
    returns: ULTPlan instance"""

    def post(self, request, *args, **kwargs):
        # Checks if user has created a ULTAid, sets View ULTAid reference to None if not
        try:
            self.ultaid = ULTAid.objects.get(user=request.user)
        # Assigns user ULTAid to View ultaid if exists
        except ULTAid.DoesNotExist:
            self.ultaid = None
        # Checks if user has created a PPxAid, sets View ppxaid reference to None if not
        try:
            self.ppxaid = PPxAid.objects.get(user=request.user)
        # Assigns user PPxAid to View ppxaid if exists
        except PPxAid.DoesNotExist:
            self.ppxaid = None
        try:
            self.ultplan = ULTPlan.objects.get(user=request.user)
        except ULTPlan.DoesNotExist:
            self.ultplan = None
        if self.ultplan:
            return HttpResponseRedirect(reverse("ultplan:detail", kwargs={"pk": request.user.ultplan.pk}))
        # Checks if view ppxaid and ultaid are not None
        if self.ppxaid and self.ultaid:
            # Get ULT model from User's ULTAid decision_aid() 'drug' dict field
            ULT_model = apps.get_model("treatment", model_name=self.ultaid.decision_aid().get("drug"))
            # Get PPx model from User's PPxAid decision_aid() 'drug' dict field
            PPx_model = apps.get_model("treatment", model_name=self.ppxaid.decision_aid().get("drug"))
            # Create ULT instance from ULT_model and User's ULTAid decision_aid() 'dose' dict field
            ULT = ULT_model.objects.create(dose=self.ultaid.decision_aid().get("dose"), user=request.user)
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
                    user=request.user,
                    ppxaid=self.ppxaid,
                )
            if PPx_model == Prednisone:
                PPx = PPx_model.objects.create(
                    dose=self.ppxaid.decision_aid().get("dose"),
                    freq=self.ppxaid.decision_aid().get("freq"),
                    dose2=None,
                    freq2=None,
                    duration2=None,
                    prn=False,
                    as_prophylaxis=True,
                    user=request.user,
                    ppxaid=self.ppxaid,
                )
            else:
                PPx = PPx_model.objects.create(
                    dose=self.ppxaid.decision_aid().get("dose"), prn=False, as_prophylaxis=True, user=request.user, ppxaid=self.ppxaid
                )
            # Create ULTPlan with the User, their ULTAid and PPxAid, ULTAid decision_aid() dict fields 'goal_urate' and 'lab_interval'
            # Set last_titration to datetime.today()
            ultplan = ULTPlan.objects.create(
                user=request.user,
                goal_urate=self.ultaid.decision_aid().get("goal_urate"),
                lab_interval=self.ultaid.decision_aid().get("lab_interval"),
                last_titration=datetime.today(),
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
            # Return redirect to ultplan:detail
            messages.success(request, "ULTPlan created.")
            return HttpResponseRedirect(reverse("ultplan:detail", kwargs={"pk": ultplan.pk}))
        # These last 2 elif and else statements will only be called if a user types in the ultplan:create url rather than following the button-links displayed on their ULTAid detail page
        # If View ultaid exists but ppxaid does not, redirect to ppxaid:ultaid-create with kwargs user.ultaid.pk
        elif self.ultaid:
            return HttpResponseRedirect(reverse("ppxaid:ultaid-create", kwargs={"ultaid": self.request.user.ultaid.pk}))
        # If neither ultaid nor ppxaid exists for view, redirect to ultaid:create to start the process
        else:
            return HttpResponseRedirect(reverse("ultaid:create"))


class ULTPlanDelete(LoginRequiredMixin, DeleteView):
    model = ULTPlan

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class ULTPlanDetail(LoginRequiredMixin, DetailView):
    model = ULTPlan
