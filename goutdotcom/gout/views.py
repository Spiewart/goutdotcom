from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from gout.models import Patient, Flare, Info, Urate, Creatinine
from gout.forms import CreatePatientForm
# Create your views here.

@login_required()

def index(request):
    patient_directory = Patient.objects.all()
    patient_count = Patient.objects.all().count()

    flare_directory = Flare.objects.all()
    flare_count = Flare.objects.all().count()

    info_directory = Info.objects.all()
    high_urate = Info.objects.filter(urate__gt=6)

    # Number of visits to this view, as counted in session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'patient_directory':patient_directory,
        'patient_count':patient_count,
        'flare_directory':flare_directory,
        'flare_count':flare_count,
        'info_directory':info_directory,
        'high_urate':high_urate,
        'num_visits':num_visits,
    }

    return render(request, 'index.html', context=context)

class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient

class FlareDetailView(LoginRequiredMixin, generic.DetailView):
    model = Flare

class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Patient

class FlareListView(LoginRequiredMixin, generic.ListView):
    model = Flare

class PatientOwnerView(LoginRequiredMixin, generic.ListView):
    """Generic User-based view listing patients by User"""
    model=Patient
    template_name = 'gout/patient_owner_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Patient.objects.order_by('age').filter(owner=self.request.user)
        #return Patient.objects.filter(owner=self.request.user)

def new_patient(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = CreatePatientForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            form.cleaned_data
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/')
    # If this is a GET (or any other method) create the default form.
    else:
        form = CreatePatientForm()

    context = {
        'form': form,
    }

    return render(request, 'gout/new_patient.html', context)

class PatientCreate(CreateView):
    model = Patient
    fields = '__all__'

class PatientUpdate(UpdateView):
    model = Patient
    fields = '__all__'

class PatientDelete(DeleteView):
    model = Patient
    success_url = reverse_lazy('patients')
