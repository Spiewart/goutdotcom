from datetime import datetime

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, View

from ..ppxaid.models import PPxAid
from ..treatment.models import Colchicine
from ..ultaid.models import ULTAid
from .models import ULTPlan

# Create your views here.


class ULTPlanCreate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            self.ppxaid = PPxAid.objects.get(user=request.user)
        except PPxAid.objects.get(user=request.user).DoesNotExist:
            self.ppxaid = None
        try:
            self.ultaid = ULTAid.objects.get(user=request.user)
        except ULTAid.objects.get(user=request.user).DoesNotExist:
            self.ultaid = None
        if self.ppxaid and self.ultaid:
            ULT_model = apps.get_model("treatment", model_name=self.ultaid.decision_aid().get("drug"))
            PPx_model = apps.get_model("treatment", model_name=self.ppxaid.decision_aid().get("drug"))
            ULT = ULT_model.objects.create(dose=self.ultaid.decision_aid().get("dose"), user=request.user)
            if PPx_model == Colchicine:
                if self.ppxaid.PPx_model:
                    PPx = self.ppxaid.PPx_model
                else:
                    PPx = PPx_model.objects.create(
                        dose=self.ppxaid.decision_aid().get("dose"),
                        freq=self.ppxaid.decision_aid().get("freq"),
                        dose2=None,
                        dose3=None,
                        user=request.user,
                    )
            PPx = PPx_model.objects.create(dose=self.ppxaid.decision_aid().get("dose"), user=request.user)
            ultplan = ULTPlan.objects.create(
                user=request.user,
                ultaid=self.ultaid,
                ppxaid=self.ppxaid,
                goal_urate=self.ultaid.decision_aid().get("goal_urate"),
                lab_interval=self.ultaid.decision_aid().get("lab_interval"),
                last_titration=datetime.today(),
            )
            ULT.ultplan = ultplan
            ULT.save()
            PPx.ultplan = ultplan
            PPx.save()
            return HttpResponseRedirect(reverse("ultplan:detail", kwargs={"pk": ultplan.pk}))
        elif self.ultaid:
            return HttpResponseRedirect(
                reverse("ppxaid:ultaid-create", kwargs={"pk": self.kwargs["pk"], "ultaid": self.request.user.ultaid.pk})
            )
        else:
            return HttpResponseRedirect(reverse("ultaid:create"))


class ULTPlanDetail(LoginRequiredMixin, DetailView):
    model = ULTPlan
