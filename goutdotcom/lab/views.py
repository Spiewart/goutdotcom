from datetime import datetime, timedelta, timezone

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
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
    LabCheckForm,
    PlateletForm,
    UrateForm,
    WBCForm,
)
from .models import ALT, AST, WBC, Creatinine, Hemoglobin, LabCheck, Platelet, Urate


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
        if self.kwargs["lab"] == "labcheck":
            template = "lab/labcheck_list.html"
        else:
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
            self.ultplan = self.request.user.ultplan
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


class LabCheckCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = LabCheck

    form_class = LabCheckForm
    alt_form_class = ALTForm
    ast_form_class = ASTForm
    creatinine_form_class = CreatinineForm
    hemoglobin_form_class = HemoglobinForm
    platelet_form_class = PlateletForm
    wbc_form_class = WBCForm
    urate_form_class = UrateForm

    def form_valid(self, form):
        # Assign LabCheck instance User and ULTPlan based off request.user
        form.instance.user = self.request.user
        form.instance.ultplan = self.request.user.ultplan
        try:
            self.alt = form.instance.alt
        except:
            self.alt = None
        try:
            self.ast = form.instance.ast
        except:
            self.ast = None
        try:
            self.creatinine = form.instance.creatinine
        except:
            self.creatinine = None
        try:
            self.hemoglobin = form.instance.hemoglobin
        except:
            self.hemoglobin = None
        try:
            self.platelet = form.instance.platelet
        except:
            self.platelet = None
        try:
            self.wbc = form.instance.wbc
        except:
            self.wbc = None
        try:
            self.urate = form.instance.urate
        except:
            self.urate = None
        # If all related models exist, mark LabCheck completed as of today's date
        if self.alt and self.ast and self.creatinine and self.hemoglobin and self.platelet and self.wbc and self.urate:
            form.instance.completed = True
            form.instance.completed_date = datetime.today().date()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Update context with related models forms. NEED to use prefix on GET to get the form inputs associated with the correct model
        context = super(LabCheckCreate, self).get_context_data(**kwargs)
        if "alt_form" not in context:
            context["alt_form"] = self.alt_form_class(self.request.GET, prefix="alt_form")
        if "ast_form" not in context:
            context["ast_form"] = self.ast_form_class(self.request.GET, prefix="ast_form")
        if "creatinine_form" not in context:
            context["creatinine_form"] = self.creatinine_form_class(self.request.GET, prefix="creatinine_form")
        if "hemoglobin_form" not in context:
            context["hemoglobin_form"] = self.hemoglobin_form_class(self.request.GET, prefix="hemoglobin_form")
        if "platelet_form" not in context:
            context["platelet_form"] = self.platelet_form_class(self.request.GET, prefix="platelet_form")
        if "wbc_form" not in context:
            context["wbc_form"] = self.wbc_form_class(self.request.GET, prefix="wbc_form")
        if "urate_form" not in context:
            context["urate_form"] = self.urate_form_class(self.request.GET, prefix="urate_form")
        return context

    def get_object(self):
        object = self.model
        return object

    def get_template_names(self):
        template = "lab/labcheck_form.html"
        return template

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=LabCheck(), prefix="labcheck_form")
        alt_form = self.alt_form_class(request.POST, instance=ALT(), prefix="alt_form")
        ast_form = self.ast_form_class(request.POST, instance=AST(), prefix="ast_form")
        creatinine_form = self.creatinine_form_class(request.POST, instance=Creatinine(), prefix="creatinine_form")
        hemoglobin_form = self.hemoglobin_form_class(request.POST, instance=Hemoglobin(), prefix="hemoglobin_form")
        platelet_form = self.platelet_form_class(request.POST, instance=Platelet(), prefix="platelet_form")
        wbc_form = self.wbc_form_class(request.POST, instance=WBC(), prefix="wbc_form")
        urate_form = self.urate_form_class(request.POST, instance=Urate(), prefix="urate_form")
        if form.is_valid():
            form_data = form.save(commit=False)
            if alt_form.is_valid():
                ALT_data = alt_form.save(commit=False)
                if ALT_data.value:
                    ALT_data.ultplan = request.user.ultplan
                    ALT_data.user = request.user
                    ALT_data.save()
                    form_data.alt = ALT_data
                else:
                    form_data.alt = None
            if ast_form.is_valid():
                AST_data = ast_form.save(commit=False)
                if AST_data.value:
                    AST_data.ultplan = request.user.ultplan
                    AST_data.user = request.user
                    AST_data.save()
                    form_data.ast = AST_data
                else:
                    form_data.ast = None
            if creatinine_form.is_valid():
                creatinine_data = creatinine_form.save(commit=False)
                if creatinine_data.value:
                    creatinine_data.ultplan = request.user.ultplan
                    creatinine_data.user = request.user
                    creatinine_data.save()
                    form_data.creatinine = creatinine_data
                else:
                    form_data.creatinine = None
            if hemoglobin_form.is_valid():
                hemoglobin_data = hemoglobin_form.save(commit=False)
                if hemoglobin_data.value:
                    hemoglobin_data.ultplan = request.user.ultplan
                    hemoglobin_data.user = request.user
                    hemoglobin_data.save()
                    form_data.hemoglobin = hemoglobin_data
                else:
                    form_data.hemoglobin = None
            if platelet_form.is_valid():
                platelet_data = platelet_form.save(commit=False)
                if platelet_data.value:
                    platelet_data.ultplan = request.user.ultplan
                    platelet_data.user = request.user
                    platelet_data.save()
                    form_data.platelet = platelet_data
                else:
                    form_data.platelet = None
            if wbc_form.is_valid():
                WBC_data = wbc_form.save(commit=False)
                if WBC_data.value:
                    WBC_data.ultplan = request.user.ultplan
                    WBC_data.user = request.user
                    WBC_data.save()
                    form_data.wbc = WBC_data
                else:
                    form_data.wbc = None
            if urate_form.is_valid():
                urate_data = urate_form.save(commit=False)
                if urate_data.value:
                    urate_data.ultplan = request.user.ultplan
                    urate_data.user = request.user
                    urate_data.save()
                    form_data.urate = urate_data
                else:
                    form_data.urate = None
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=self.form_class(request.POST, instance=LabCheck()),
                    alt_form=self.alt_form_class(request.POST, instance=ALT()),
                    ast_form=self.ast_form_class(request.POST, instance=AST()),
                    creatinine_form=self.creatinine_form_class(request.POST, instance=Creatinine()),
                    hemoglobin_form=self.hemoglobin_form_class(request.POST, instance=Hemoglobin()),
                    platelet_form=self.platelet_form_class(request.POST, instance=Platelet()),
                    WBC_form=self.wbc_form_class(request.POST, instance=Platelet()),
                    urate_form=self.urate_form_class(request.POST, instance=Urate()),
                )
            )


class LabCheckUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LabCheck

    form_class = LabCheckForm
    alt_form_class = ALTForm
    ast_form_class = ASTForm
    creatinine_form_class = CreatinineForm
    hemoglobin_form_class = HemoglobinForm
    platelet_form_class = PlateletForm
    wbc_form_class = WBCForm
    urate_form_class = UrateForm

    def form_valid(self, form):
        # Assign LabCheck instance User and ULTPlan based off request.user
        form.instance.user = self.request.user
        form.instance.ultplan = self.request.user.ultplan
        try:
            self.alt = form.instance.alt
        except:
            self.alt = None
        try:
            self.ast = form.instance.ast
        except:
            self.ast = None
        try:
            self.creatinine = form.instance.creatinine
        except:
            self.creatinine = None
        try:
            self.hemoglobin = form.instance.hemoglobin
        except:
            self.hemoglobin = None
        try:
            self.platelet = form.instance.platelet
        except:
            self.platelet = None
        try:
            self.wbc = form.instance.wbc
        except:
            self.wbc = None
        try:
            self.urate = form.instance.urate
        except:
            self.urate = None
        # If all related models exist, mark LabCheck completed as of today's date
        if self.alt and self.ast and self.creatinine and self.hemoglobin and self.platelet and self.wbc and self.urate:
            form.instance.completed = True
            # MUST call date(), otherwise functions comparing dates will throw errors for comparing datetime.datetime types to datetime.date types
            form.instance.completed_date = datetime.today().date()
            # Run LabCheck check_for_abnormal_labs() function, titrate() will be called by the check_for_abnormal_labs() if appropriate
            form.instance.ultplan.check_for_abnormal_labs(form.instance)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Long block of try/except statements to determine if LabCheck has associated lab models
        try:
            self.alt = self.object.alt
        except:
            self.alt = None
        try:
            self.ast = self.object.ast
        except:
            self.ast = None
        try:
            self.creatinine = self.object.creatinine
        except:
            self.creatinine = None
        try:
            self.hemoglobin = self.object.hemoglobin
        except:
            self.hemoglobin = None
        try:
            self.platelet = self.object.platelet
        except:
            self.platelet = None
        try:
            self.wbc = self.object.wbc
        except:
            self.wbc = None
        try:
            self.urate = self.object.urate
        except:
            self.urate = None
        # Update context with related models forms, with existing instance if it exists, otherwise a new instance. NEED to use prefix on GET to get the form inputs associated with the correct model.
        context = super(LabCheckUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            if "alt_form" not in context:
                if self.alt:
                    context["alt_form"] = self.alt_form_class(self.request.POST, instance=self.alt, prefix="alt_form")
                else:
                    context["alt_form"] = self.alt_form_class(self.request.POST, instance=ALT(), prefix="alt_form")
            if "ast_form" not in context:
                if self.ast:
                    context["ast_form"] = self.ast_form_class(self.request.POST, instance=self.ast, prefix="ast_form")
                else:
                    context["ast_form"] = self.ast_form_class(self.request.POST, instance=AST(), prefix="ast_form")
            if "creatinine_form" not in context:
                if self.creatinine:
                    context["creatinine_form"] = self.creatinine_form_class(
                        self.request.POST, instance=self.creatinine, prefix="creatinine_form"
                    )
                else:
                    context["creatinine_form"] = self.creatinine_form_class(
                        self.request.POST, instance=Creatinine(), prefix="creatinine_form"
                    )
            if "hemoglobin_form" not in context:
                if self.hemoglobin:
                    context["hemoglobin_form"] = self.hemoglobin_form_class(
                        self.request.POST, instance=self.hemoglobin, prefix="hemoglobin_form"
                    )
                else:
                    context["hemoglobin_form"] = self.hemoglobin_form_class(
                        self.request.POST, instance=Hemoglobin(), prefix="hemoglobin_form"
                    )
            if "platelet_form" not in context:
                if self.platelet:
                    context["platelet_form"] = self.platelet_form_class(
                        self.request.POST, instance=self.platelet, prefix="platelet_form"
                    )
                else:
                    context["platelet_form"] = self.platelet_form_class(
                        self.request.POST, instance=Platelet(), prefix="platelet_form"
                    )
            if "wbc_form" not in context:
                if self.wbc:
                    context["wbc_form"] = self.wbc_form_class(self.request.POST, instance=self.wbc, prefix="wbc_form")
                else:
                    context["wbc_form"] = self.wbc_form_class(self.request.POST, instance=WBC(), prefix="wbc_form")
            if "urate_form" not in context:
                if self.urate:
                    context["urate_form"] = self.urate_form_class(
                        self.request.POST, instance=self.urate, prefix="urate_form"
                    )
                else:
                    context["urate_form"] = self.urate_form_class(
                        self.request.POST, instance=Urate(), prefix="urate_form"
                    )
            return context
        else:
            if "alt_form" not in context:
                if self.alt:
                    context["alt_form"] = self.alt_form_class(instance=self.alt, prefix="alt_form")
                else:
                    context["alt_form"] = self.alt_form_class(instance=ALT(), prefix="alt_form")
            if "ast_form" not in context:
                if self.ast:
                    context["ast_form"] = self.ast_form_class(instance=self.ast, prefix="ast_form")
                else:
                    context["ast_form"] = self.ast_form_class(instance=AST(), prefix="ast_form")
            if "creatinine_form" not in context:
                if self.creatinine:
                    context["creatinine_form"] = self.creatinine_form_class(
                        instance=self.creatinine, prefix="creatinine_form"
                    )
                else:
                    context["creatinine_form"] = self.creatinine_form_class(
                        instance=Creatinine(), prefix="creatinine_form"
                    )
            if "hemoglobin_form" not in context:
                if self.hemoglobin:
                    context["hemoglobin_form"] = self.hemoglobin_form_class(
                        instance=self.hemoglobin, prefix="hemoglobin_form"
                    )
                else:
                    context["hemoglobin_form"] = self.hemoglobin_form_class(
                        instance=Hemoglobin(), prefix="hemoglobin_form"
                    )
            if "platelet_form" not in context:
                if self.platelet:
                    context["platelet_form"] = self.platelet_form_class(instance=self.platelet, prefix="platelet_form")
                else:
                    context["platelet_form"] = self.platelet_form_class(instance=Platelet(), prefix="platelet_form")
            if "wbc_form" not in context:
                if self.wbc:
                    context["wbc_form"] = self.wbc_form_class(instance=self.wbc, prefix="wbc_form")
                else:
                    context["wbc_form"] = self.wbc_form_class(instance=WBC(), prefix="wbc_form")
            if "urate_form" not in context:
                if self.urate:
                    context["urate_form"] = self.urate_form_class(instance=self.urate, prefix="urate_form")
                else:
                    context["urate_form"] = self.urate_form_class(instance=Urate(), prefix="urate_form")
            return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        alt_form = self.alt_form_class(request.POST, instance=self.object.alt, prefix="alt_form")
        ast_form = self.ast_form_class(request.POST, instance=self.object.ast, prefix="ast_form")
        creatinine_form = self.creatinine_form_class(
            request.POST, instance=self.object.creatinine, prefix="creatinine_form"
        )
        hemoglobin_form = self.hemoglobin_form_class(
            request.POST, instance=self.object.hemoglobin, prefix="hemoglobin_form"
        )
        platelet_form = self.platelet_form_class(request.POST, instance=self.object.platelet, prefix="platelet_form")
        wbc_form = self.wbc_form_class(request.POST, instance=self.object.wbc, prefix="wbc_form")
        urate_form = self.urate_form_class(request.POST, instance=self.object.urate, prefix="urate_form")
        if form.is_valid():
            form_data = form.save(commit=False)
            if alt_form.is_valid():
                ALT_data = alt_form.save(commit=False)
                if ALT_data.value:
                    ALT_data.ultplan = request.user.ultplan
                    ALT_data.user = request.user
                    ALT_data.save()
                    form_data.alt = ALT_data
                else:
                    form_data.alt = None
            if ast_form.is_valid():
                AST_data = ast_form.save(commit=False)
                if AST_data.value:
                    AST_data.ultplan = request.user.ultplan
                    AST_data.user = request.user
                    AST_data.save()
                    form_data.ast = AST_data
                else:
                    form_data.ast = None
            if creatinine_form.is_valid():
                creatinine_data = creatinine_form.save(commit=False)
                if creatinine_data.value:
                    creatinine_data.ultplan = request.user.ultplan
                    creatinine_data.user = request.user
                    creatinine_data.save()
                    form_data.creatinine = creatinine_data
                else:
                    form_data.creatinine = None
            if hemoglobin_form.is_valid():
                hemoglobin_data = hemoglobin_form.save(commit=False)
                if hemoglobin_data.value:
                    hemoglobin_data.ultplan = request.user.ultplan
                    hemoglobin_data.user = request.user
                    hemoglobin_data.save()
                    form_data.hemoglobin = hemoglobin_data
                else:
                    form_data.hemoglobin = None
            if platelet_form.is_valid():
                platelet_data = platelet_form.save(commit=False)
                if platelet_data.value:
                    platelet_data.ultplan = request.user.ultplan
                    platelet_data.user = request.user
                    platelet_data.save()
                    form_data.platelet = platelet_data
                else:
                    form_data.platelet = None
            if wbc_form.is_valid():
                WBC_data = wbc_form.save(commit=False)
                if WBC_data.value:
                    WBC_data.ultplan = request.user.ultplan
                    WBC_data.user = request.user
                    WBC_data.save()
                    form_data.wbc = WBC_data
                else:
                    form_data.wbc = None
            if urate_form.is_valid():
                urate_data = urate_form.save(commit=False)
                if urate_data.value:
                    urate_data.ultplan = request.user.ultplan
                    urate_data.user = request.user
                    urate_data.save()
                    form_data.urate = urate_data
                else:
                    form_data.urate = None
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    alt_form=self.alt_form_class(request.POST, instance=ALT()),
                    ast_form=self.ast_form_class(request.POST, instance=AST()),
                    creatinine_form=self.creatinine_form_class(request.POST, instance=Creatinine()),
                    hemoglobin_form=self.hemoglobin_form_class(request.POST, instance=Hemoglobin()),
                    platelet_form=self.platelet_form_class(request.POST, instance=Platelet()),
                    WBC_form=self.wbc_form_class(request.POST, instance=Platelet()),
                    urate_form=self.urate_form_class(request.POST, instance=Urate()),
                )
            )
