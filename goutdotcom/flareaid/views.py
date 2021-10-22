from django.http.response import Http404
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import FlareAidForm
from .models import FlareAid


# Create your views here.
class FlareAidCreate(CreateView):
    model = FlareAid
    form_class = FlareAidForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)


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
