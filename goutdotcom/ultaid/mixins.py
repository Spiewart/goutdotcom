from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.utils.functional import cached_property
from django.views.generic.base import ContextMixin, View

from ..ult.models import ULT


class ULTMixin(ContextMixin, View):
    """Mixin that checks for a ult kwarg and tries to fetch a ULT with it.
    Adds the ULT to object instance to be called as a property.
    Avoids multiple queries to DB.
    Adds ULT object to context

    Returns:
        [ULT or None]: [Returns a ULT object or None]
    """

    @cached_property
    def ult(self):
        self.ult_kwarg = None
        self.ult = None
        try:
            self.ult_kwarg = self.kwargs.get("ult", None)
        except ObjectDoesNotExist:
            self.ult_kwarg = None
        if self.ult_kwarg:
            if isinstance(self.ult_kwarg, int):
                try:
                    self.ult = ULT.objects.get(pk=self.ult_kwarg)
                except ULT.DoesNotExist:
                    raise Http404("No ULT that matches that query")
            else:
                try:
                    self.ult = ULT.objects.get(slug=self.ult_kwarg)
                except ULT.DoesNotExist:
                    raise Http404("No ULT that matches that query")
        return self.ult

    def get_context_data(self, **kwargs):
        context = super(ULTMixin, self).get_context_data(**kwargs)
        context["ult"] = self.ult
        return context
