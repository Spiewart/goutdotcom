from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..history.forms import CKDForm
from ..history.models import CKD
from .forms import FlareAidForm
from .models import FlareAid


# Create your views here.
class FlareAidCreate(CreateView):
    model = FlareAid
    form_class = FlareAidForm
    CKD_form_class = CKDForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.instance.ckd = self.request.user.medicalprofile.ckd
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FlareAidCreate, self).get_context_data(**kwargs)
        if "CKD_form" not in context:
            context["CKD_form"] = self.CKD_form_class(instance=self.request.user.medicalprofile.CKD)
        return context

    def get_form_kwargs(self):
        kwargs = super(FlareAidCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user  # pass the 'user' in kwargs
        return kwargs

    def post(self, request):
        form = self.form_class(request.POST, instance=FlareAid())

        if form.is_valid():
            flareaid_data = form.save(commit=False)
            # Check if user is authenticated and pull CKD data from MedicalProfile if so
            if request.user.is_authenticated:
                flareaid_data.user = request.user
                CKD_form = self.CKD_form_class(request.POST, instance=request.user.medicalprofile.CKD)
                ckd_data = CKD_form.save(commit=False)
                ckd_data.last_modified = "FlareAid"
                ckd_data = CKD_form.save()
                flareaid_data.ckd = ckd_data
                flareaid_data.save()
            else:
                CKD_form = self.CKD_form_class(request.POST, instance=CKD())
                ckd_data = CKD_form.save(commit=False)
                ckd_data.last_modified = "FlareAid"
                ckd_data.save()
                flareaid_data.ckd = ckd_data
                flareaid_data.save()
            return HttpResponseRedirect(reverse("flareaid:detail", kwargs={"pk": flareaid_data.pk}))
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    CKD_form=self.CKD_form_class(request.POST, instance=CKD()),
                )
            )


class FlareAidDetail(DetailView):
    model = FlareAid
    template_name = "flareaid/flareaid_detail.html"


class FlareAidList(ListView):
    model = FlareAid
    """Changed allow_empty to = False so it returns 404 when empty, then redirect with dispatch to DecisionAid About view"""

    allow_empty = False
    paginate_by = 5
    """Overrode dispatch to redirect to Flare About view if FlareAid view returns 404, as in the case of it being empty due to allow_empty=False
    """

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Http404:
            return redirect("flare:about")

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update(
            {
                "flareaid_list": FlareAid.objects.filter(user=self.request.user),
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by("-created")


class FlareAidUpdate(UpdateView):
    model = FlareAid
    form_class = FlareAidForm
