from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import modelform_factory
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from ..ultplan.models import ULTPlan
from .forms import (
    ALTForm,
    ASTForm,
    CreatinineForm,
    HemoglobinForm,
    PlateletForm,
    UrateForm,
    WBCForm,
)
from .models import ALT, AST, WBC, Creatinine, Hemoglobin, Platelet, Urate


# Create your views here.
class LabAbout(TemplateView):
    def get_template_names(self, **kwargs):
        kwargs = self.kwargs
        lab = kwargs.get("lab")
        template = "lab/" + str(lab) + "_about.html"
        return template

    def get_context_data(self, **kwargs):
        context = super(LabAbout, self).get_context_data(**kwargs)
        context.update(
            {
                "lab": self.kwargs["lab"],
            }
        )
        return context


class LabCreate(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        self.object = None
        self.lab = self.kwargs["lab"]
        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        self.lab = self.kwargs["lab"]
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured("Specifying both 'fields' and 'form_class' is not permitted.")
        if self.form_class:
            return self.form_class
        else:
            if self.lab is not None:
                # Fetch model from URL 'lab' parameter
                model = apps.get_model("lab", model_name=self.lab)
            elif getattr(self, "object", None) is not None:
                model = self.object.__class__
            else:
                model = self.get_queryset().model
            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )
            return modelform_factory(model, fields=self.fields)

    def get_template_names(self):
        template = "lab/lab_form_base.html"
        return template

    fields = [
        "value",
        "date_drawn",
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LabCreate, self).get_context_data(**kwargs)
        context.update(
            {
                "lab": self.kwargs["lab"],
            }
        )
        return context


class LabDetail(LoginRequiredMixin, DetailView):
    def get_object(self):
        self.model = apps.get_model("lab", model_name=self.kwargs["lab"])
        lab = get_object_or_404(self.model, pk=self.kwargs["pk"], user=self.request.user)
        return lab

    def get_template_names(self):
        template = "lab/lab_detail_base.html"
        return template


class LabList(LoginRequiredMixin, ListView):
    paginate_by = 5

    def get_queryset(self):
        self.model = apps.get_model("lab", model_name=self.kwargs["lab"])
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.filter(user=self.request.user).order_by("-created")
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
                )
        return self.queryset.filter(user=self.request.user).order_by("-created")

    def get_template_names(self, **kwargs):
        template = "lab/lab_list_base.html"
        return template

    def get_context_data(self, **kwargs):
        self.model = apps.get_model("lab", model_name=self.kwargs["lab"])
        context = super(LabList, self).get_context_data(**kwargs)
        context.update(
            {
                "lab": self.kwargs["lab"],
            }
        )
        return context


class LabUpdate(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        self.lab = self.kwargs["lab"]
        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        self.lab = self.kwargs["lab"]
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured("Specifying both 'fields' and 'form_class' is not permitted.")
        if self.form_class:
            return self.form_class
        else:
            if self.lab is not None:
                # Fetch model from URL 'lab' parameter
                model = apps.get_model("lab", model_name=self.lab)
            elif getattr(self, "object", None) is not None:
                model = self.object.__class__
            else:
                model = self.get_queryset().model
            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )
            return modelform_factory(model, fields=self.fields)

    def get_template_names(self):
        template = "lab/lab_form_base.html"
        return template

    fields = [
        "value",
        "date_drawn",
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LabUpdate, self).get_context_data(**kwargs)
        context.update(
            {
                "lab": self.kwargs["lab"],
            }
        )
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs["pk"]
        model = apps.get_model("lab", model_name=self.kwargs["lab"])
        try:
            queryset = model.objects.filter(user=self.request.user, pk=pk)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")
        obj = super(LabUpdate, self).get_object(queryset=queryset)
        return obj


class IndexView(LoginRequiredMixin, ListView):
    template_name = "lab/index.html"
    model = Urate

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            {
                "urate_list": Urate.objects.filter(user=self.request.user).order_by("-date_drawn")[:1],
                "ALT_list": ALT.objects.filter(user=self.request.user).order_by("-date_drawn")[:1],
                "AST_list": AST.objects.filter(user=self.request.user).order_by("-date_drawn")[:1],
                "platelet_list": Platelet.objects.filter(user=self.request.user).order_by("-date_drawn")[:1],
                "WBC_list": WBC.objects.filter(user=self.request.user).order_by("-date_drawn")[:1],
                "hemoglobin_list": Hemoglobin.objects.filter(user=self.request.user).order_by("-date_drawn")[:1],
                "creatinine_list": Creatinine.objects.filter(user=self.request.user).order_by("-date_drawn")[:1],
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ULTPlanCreate(CreateView):
    model = ALT
    form_class = ALTForm
    AST_form_class = ASTForm
    creatinine_form_class = CreatinineForm
    hemoglobin_form_class = HemoglobinForm
    platelet_form_class = PlateletForm
    WBC_form_class = WBCForm
    urate_form_class = UrateForm

    def form_valid(self, form):
        # Fetch ULTForm.pk from **kwargs, assign to form instance
        self.ultplan = ULTPlan.objects.get(pk=self.kwargs.get("ultplan"))
        form.instance.ultplan = self.ultplan
        # Check if user is authenticated, assign to form instance if so
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ULTPlanCreate, self).get_context_data(**kwargs)
        if "ALT_form" not in context:
            context["ALT_form"] = self.form_class(self.request.GET)
        if "AST_form" not in context:
            context["AST_form"] = self.AST_form_class(self.request.GET)
        if "creatinine_form" not in context:
            context["creatinine_form"] = self.creatinine_form_class(self.request.GET)
        if "hemoglobin_form" not in context:
            context["hemoglobin_form"] = self.hemoglobin_form_class(self.request.GET)
        if "platelet_form" not in context:
            context["platelet_form"] = self.platelet_form_class(self.request.GET)
        if "WBC_form" not in context:
            context["WBC_form"] = self.WBC_form_class(self.request.GET)
        if "urate_form" not in context:
            context["urate_form"] = self.urate_form_class(self.request.GET)
        return context

    def get_object(self):
        object = self.model
        return object

    def get_template_names(self):
        template = "lab/ultplan_form.html"
        return template

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        ALT_form = self.form_class(request.POST, instance=ALT(), prefix="ALT_form")
        AST_form = self.AST_form_class(request.POST, instance=AST(), prefix="AST_form")
        creatinine_form = self.creatinine_form_class(request.POST, instance=Creatinine(), prefix="creatinine_form")
        hemoglobin_form = self.hemoglobin_form_class(request.POST, instance=Hemoglobin(), prefix="hemoglobin_form")
        platelet_form = self.platelet_form_class(request.POST, instance=Platelet(), prefix="platelet_form")
        WBC_form = self.WBC_form_class(request.POST, instance=Platelet(), prefix="WBC_form")
        urate_form = self.urate_form_class(request.POST, instance=Urate(), prefix="urate_form")

        if (
            ALT_form.is_valid()
            and AST_form.is_valid()
            and creatinine_form.is_valid()
            and hemoglobin_form.is_valid()
            and platelet_form.is_valid()
            and WBC_form.is_valid()
            and urate_form.is_valid()
        ):
            ultplan = ULTPlan.objects.get(pk=kwargs["ultplan"])
            ALT_data = ALT_form.save()
            ALT_data.ultplan = ultplan
            ALT_data.user = request.user
            ALT_data.save()
            AST_data = AST_form.save(commit=False)
            AST_data.ultplan = ultplan
            AST_data.user = request.user
            AST_data.save()
            creatinine_data = creatinine_form.save(commit=False)
            creatinine_data.ultplan = ultplan
            creatinine_data.user = request.user
            creatinine_data.save()
            hemoglobin_data = hemoglobin_form.save(commit=False)
            hemoglobin_data.ultplan = ultplan
            hemoglobin_data.user = request.user
            hemoglobin_data.save()
            platelet_data = platelet_form.save(commit=False)
            platelet_data.ultplan = ultplan
            platelet_data.user = request.user
            platelet_data.save()
            WBC_data = WBC_form.save(commit=False)
            WBC_data.ultplan = ultplan
            WBC_data.user = request.user
            WBC_data.save()
            urate_data = urate_form.save(commit=False)
            urate_data.ultplan = ultplan
            urate_data.user = request.user
            urate_data.save()
            return self.form_valid(ALT_form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    ALT_form=self.form_class(request.POST, instance=ALT()),
                    AST_form=self.AST_form_class(request.POST, instance=AST()),
                    creatinine_form=self.creatinine_form_class(request.POST, instance=Creatinine()),
                    hemoglobin_form=self.hemoglobin_form_class(request.POST, instance=Hemoglobin()),
                    platelet_form=self.platelet_form_class(request.POST, instance=Platelet()),
                    WBC_form=self.WBC_form_class(request.POST, instance=Platelet()),
                    urate_form=self.urate_form_class(request.POST, instance=Urate()),
                )
            )
