from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from .models import ALT, AST, Creatinine, Hemoglobin, Platelet, Urate, WBC

# Create your views here.
class LabAbout(TemplateView):
    def get_template_names(self, **kwargs):
        kwargs = self.kwargs
        lab = kwargs.get('lab')
        template = "lab/" + str(lab) + "_about.html"
        return template

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'lab/index.html'
    model = Urate

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'urate_list': Urate.objects.filter(user=self.request.user).order_by('-created')[:3],
            'ALT_list': ALT.objects.filter(user=self.request.user).order_by('-created')[:3],
            'AST_list': AST.objects.filter(user=self.request.user).order_by('-created')[:3],
            'platelet_list': Platelet.objects.filter(user=self.request.user).order_by('-created')[:3],
            'WBC_list': WBC.objects.filter(user=self.request.user).order_by('-created')[:3],
            'hemoglobin_list': Hemoglobin.objects.filter(user=self.request.user).order_by('-created')[:3],
            'creatinine_list': Creatinine.objects.filter(user=self.request.user).order_by('-created')[:3],
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class UrateCreate(LoginRequiredMixin, CreateView):
    model = Urate
    fields = ['value', 'date_drawn',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UrateDetail(LoginRequiredMixin, DetailView):
    model = Urate

class UrateList(LoginRequiredMixin, ListView):
    model = Urate
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'urate_list': Urate.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class UrateUpdate(LoginRequiredMixin, UpdateView):
    model = Urate
    fields = ['value', 'date_drawn',]
    template_name = 'lab/urate_update.html'

class ALTCreate(LoginRequiredMixin, CreateView):
    model = ALT
    fields = ['value', 'date_drawn']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ALTDetail(LoginRequiredMixin, DetailView):
    model = ALT

class ALTList(LoginRequiredMixin, ListView):
    model = ALT
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'ALT_list': ALT.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class ALTUpdate(LoginRequiredMixin, UpdateView):
    model = ALT
    fields = ['value', 'date_drawn']
    template_name = 'lab/ALT_update.html'

class ASTCreate(LoginRequiredMixin, CreateView):
    model = AST
    fields = ['value', 'date_drawn']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ASTDetail(LoginRequiredMixin, DetailView):
    model = AST

class ASTList(LoginRequiredMixin, ListView):
    model = AST
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'AST_list': AST.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class ASTUpdate(LoginRequiredMixin, UpdateView):
    model = AST
    fields = ['value', 'date_drawn']
    template_name = 'lab/AST_update.html'

class PlateletCreate(LoginRequiredMixin, CreateView):
    model = Platelet
    fields = ['value', 'date_drawn']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlateletDetail(LoginRequiredMixin, DetailView):
    model = Platelet

class PlateletList(LoginRequiredMixin, ListView):
    model = Platelet
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'platelet_list': Platelet.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class PlateletUpdate(LoginRequiredMixin, UpdateView):
    model = Platelet
    fields = ['value', 'date_drawn']
    template_name = 'lab/platelet_update.html'

class WBCCreate(LoginRequiredMixin, CreateView):
    model = WBC
    fields = ['value', 'date_drawn']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WBCDetail(LoginRequiredMixin, DetailView):
    model = WBC

class WBCList(LoginRequiredMixin, ListView):
    model = WBC
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'WBC_list': WBC.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class WBCUpdate(LoginRequiredMixin, UpdateView):
    model = WBC
    fields = ['value', 'date_drawn']
    template_name = 'lab/WBC_update.html'

class HemoglobinCreate(LoginRequiredMixin, CreateView):
    model = Hemoglobin
    fields = ['value', 'date_drawn']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HemoglobinDetail(LoginRequiredMixin, DetailView):
    model = Hemoglobin

class HemoglobinList(LoginRequiredMixin, ListView):
    model = Hemoglobin
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'hemoglobin_list': Hemoglobin.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class HemoglobinUpdate(LoginRequiredMixin, UpdateView):
    model = Hemoglobin
    fields = ['value', 'date_drawn']
    template_name = 'lab/hemoglobin_update.html'

class CreatinineCreate(LoginRequiredMixin, CreateView):
    model = Creatinine
    fields = ['value', 'date_drawn']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CreatinineDetail(LoginRequiredMixin, DetailView):
    model = Creatinine

class CreatinineList(LoginRequiredMixin, ListView):
    model = Creatinine
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'creatinine_list': Creatinine.objects.filter(user=self.request.user),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created')

class CreatinineUpdate(LoginRequiredMixin, UpdateView):
    model = Creatinine
    fields = ['value', 'date_drawn']
    template_name = 'lab/creatinine_update.html'
