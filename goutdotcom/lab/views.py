from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import ALT, AST, Creatinine, Hemoglobin, Platelet, Urate, WBC

# Create your views here.
class IndexView(ListView):
    template_name = 'lab/index.html'
    model = Urate

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'urate_list': Urate.objects.filter(user=self.request.user),
            'creatinine_list': Creatinine.objects.filter(user=self.request.user), 
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

def log(request):
    return render(request, 'log.html')

class UrateCreate(LoginRequiredMixin, CreateView):
    model = Urate
    fields = ['uric_acid']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UrateDetail(LoginRequiredMixin, DetailView):
    model = Urate

class UrateList(LoginRequiredMixin, ListView):
    model = Urate

class UrateUpdate(LoginRequiredMixin, UpdateView):
    model = Urate
    fields = ['uric_acid']
    template_name = 'lab/urate_update.html'

class ALTCreate(LoginRequiredMixin, CreateView):
    model = ALT
    fields = ['alt_sgpt']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ALTDetail(LoginRequiredMixin, DetailView):
    model = ALT

class ALTList(LoginRequiredMixin, ListView):
    model = ALT

class ALTUpdate(LoginRequiredMixin, UpdateView):
    model = ALT
    fields = ['alt_sgpt']
    template_name = 'lab/ALT_update.html'

class ASTCreate(LoginRequiredMixin, CreateView):
    model = AST
    fields = ['ast_sgot']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ASTDetail(LoginRequiredMixin, DetailView):
    model = AST

class ASTList(LoginRequiredMixin, ListView):
    model = AST

class ASTUpdate(LoginRequiredMixin, UpdateView):
    model = AST
    fields = ['ast_sgot']
    template_name = 'lab/AST_update.html'

class PlateletCreate(LoginRequiredMixin, CreateView):
    model = Platelet
    fields = ['platelets']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlateletDetail(LoginRequiredMixin, DetailView):
    model = Platelet

class PlateletList(LoginRequiredMixin, ListView):
    model = Platelet

class PlateletUpdate(LoginRequiredMixin, UpdateView):
    model = Platelet
    fields = ['platelets']
    template_name = 'lab/platelet_update.html'

class WBCCreate(LoginRequiredMixin, CreateView):
    model = WBC
    fields = ['white_blood_cells']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WBCDetail(LoginRequiredMixin, DetailView):
    model = WBC

class WBCList(LoginRequiredMixin, ListView):
    model = WBC

class WBCUpdate(LoginRequiredMixin, UpdateView):
    model = WBC
    fields = ['white_blood_cells']
    template_name = 'lab/WBC_update.html'

class HemoglobinCreate(LoginRequiredMixin, CreateView):
    model = Hemoglobin
    fields = ['hemoglobin']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HemoglobinDetail(LoginRequiredMixin, DetailView):
    model = Hemoglobin

class HemoglobinList(LoginRequiredMixin, ListView):
    model = Hemoglobin

class HemoglobinUpdate(LoginRequiredMixin, UpdateView):
    model = Hemoglobin
    fields = ['hemoglobin']
    template_name = 'lab/hemoglobin_update.html'

class CreatinineCreate(LoginRequiredMixin, CreateView):
    model = Creatinine
    fields = ['creatinine']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CreatinineDetail(LoginRequiredMixin, DetailView):
    model = Creatinine

class CreatinineList(LoginRequiredMixin, ListView):
    model = Creatinine

class CreatinineUpdate(LoginRequiredMixin, UpdateView):
    model = Creatinine
    fields = ['creatinine']
    template_name = 'lab/creatinine_update.html'