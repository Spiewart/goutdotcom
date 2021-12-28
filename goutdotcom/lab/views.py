from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import modelform_factory
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
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


class LabCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
        # Check if ultplan kwarg was sent via the url and, if so, assign it to the lab ultplan via the template button => POST request
        if self.kwargs.get("ultplan"):
            form.instance.ultplan = ULTPlan.objects.get(pk=self.kwargs.get("ultplan"))
        form.instance.user = self.request.user
        messages.success(self.request, f"{self.kwargs['lab'].capitalize()} created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LabCreate, self).get_context_data(**kwargs)
        context.update(
            {
                "lab": self.kwargs["lab"],
            }
        )
        return context

    def get_success_url(self):
        if self.kwargs.get("ultplan"):
            return reverse("ultplan:detail", kwargs={"pk": self.kwargs["ultplan"]})
        else:
            return reverse("lab:detail", kwargs={"lab": self.kwargs["lab"], "pk": self.object.pk})


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

    def dispatch(self, *args, **kwargs):
        # Check if user has a ULTPlan, redirect to lab:about all labs if not, send message to User indicating they need to make a ULTPlan before its worth reporting
        try:
            ultplan = self.request.user.ultplan
        except ULTPlan.DoesNotExist:
            messages.info(self.request, f"No reason to have labs without a ULTPlan!")
            return redirect("lab:about", lab="alllabs")
        if self.ultplan:
            return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            {
                "labs": [
                    Urate.objects.filter(user=self.request.user, ultplan=self.request.user.ultplan).last(),
                    ALT.objects.filter(user=self.request.user, ultplan=self.request.user.ultplan).last(),
                    AST.objects.filter(user=self.request.user, ultplan=self.request.user.ultplan).last(),
                    Platelet.objects.filter(user=self.request.user, ultplan=self.request.user.ultplan).last(),
                    WBC.objects.filter(user=self.request.user, ultplan=self.request.user.ultplan).last(),
                    Hemoglobin.objects.filter(user=self.request.user, ultplan=self.request.user.ultplan).last(),
                    Creatinine.objects.filter(user=self.request.user, ultplan=self.request.user.ultplan).last(),
                ]
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
        if self.kwargs["pk"]:
            self.ultplan = ULTPlan.objects.get(pk=self.kwargs.get("pk"))
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
        ultplan = ULTPlan.objects.get(pk=kwargs["ultplan"])

        if (
            ALT_form.is_valid()
            or AST_form.is_valid()
            or creatinine_form.is_valid()
            or hemoglobin_form.is_valid()
            or platelet_form.is_valid()
            or WBC_form.is_valid()
            or urate_form.is_valid()
        ):
            if ALT_form.is_valid():
                ALT_data = ALT_form.save(commit=False)
                ALT_data.ultplan = ultplan
                ALT_data.user = request.user
                if ALT_data.value:
                    ALT_data.save()
            if AST_form.is_valid():
                AST_data = AST_form.save(commit=False)
                AST_data.ultplan = ultplan
                AST_data.user = request.user
                if AST_data.value:
                    AST_data.save()
            if creatinine_form.is_valid():
                creatinine_data = creatinine_form.save(commit=False)
                creatinine_data.ultplan = ultplan
                creatinine_data.user = request.user
                if creatinine_data.value:
                    creatinine_data.save()
            if hemoglobin_form.is_valid():
                hemoglobin_data = hemoglobin_form.save(commit=False)
                if hemoglobin_data.value:
                    hemoglobin_data.ultplan = ultplan
                    hemoglobin_data.user = request.user
                    hemoglobin_data.save()
            if platelet_form.is_valid():
                platelet_data = platelet_form.save(commit=False)
                if platelet_data.value:
                    platelet_data.ultplan = ultplan
                    platelet_data.user = request.user
                    platelet_data.save()
            if WBC_form.is_valid():
                WBC_data = WBC_form.save(commit=False)
                if WBC_data.value:
                    WBC_data.ultplan = ultplan
                    WBC_data.user = request.user
                    WBC_data.save()
            if urate_form.is_valid():
                urate_data = urate_form.save(commit=False)
                if urate_data.value:
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
