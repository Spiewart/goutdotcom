
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.utils.functional import cached_property
from django.views.generic.base import ContextMixin, View

from ..flare.models import Flare


class FlareMixin(ContextMixin, View):
    """Mixin that checks for a flare kwarg and tries to fetch a Flare with it.
    Adds the Flare to object instance to be called as a property.
    Avoids multiple queries to DB.
    Adds Flare object to context

    Returns:
        [Flare or None]: [Returns a Flare object or None]
    """

    @cached_property
    def flare(self):
        self.flare_kwarg = None
        self.flare = None
        try:
            self.flare_kwarg = self.kwargs.get("flare", None)
        except ObjectDoesNotExist:
            self.flare_kwarg = None
        if self.flare_kwarg:
            if isinstance(self.flare_kwarg, int):
                try:
                    self.flare = Flare.objects.get(pk=self.flare_kwarg)
                except Flare.DoesNotExist:
                    raise Http404("No Flare that matches that query")
            else:
                try:
                    self.flare = Flare.objects.get(slug=self.flare_kwarg)
                except Flare.DoesNotExist:
                    raise Http404("No Flare that matches that query")
        return self.flare

    def get_context_data(self, **kwargs):
        context = super(FlareMixin, self).get_context_data(**kwargs)
        context["flare"] = self.flare
        return context
