import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import PatientSignUpForm, DoctorSignUpForm, AppointmentDepartmentForm, UserUpdateForm, ProfilisUpdateForm, DoctorUpdateForm, PatientUpdateForm, PatientCardUpdateForm
from .models import User, Appointment, Doctor, Department, Service, Patient, PatientCard, InvoiceLine, Invoice, Profile
from django.views.generic import ListView, CreateView
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from django.db.models import Q
from django.utils.translation import gettext as _
import os
from clinic.email_settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

utc = pytz.UTC


def index(request):
    return render(request, 'index.html')


def select_department(request):
    if request.method == 'POST':
        form = AppointmentDepartmentForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data['department']
            return redirect(f'/appointment/new/{department}')
    else:
        form = AppointmentDepartmentForm()
    return render(request, 'select_department.html', {'form': form})


@csrf_exempt
@login_required
def new_appointment(request, department):
    try:
        if request.method == 'POST':
            date_time = request.POST['date']
            date = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")
            doctor = request.POST['doctor']
            doc = Doctor.objects.filter(name=doctor).first()
            visit_check = Appointment.objects.filter(doctor_ID=doc.user_id).all()
            for i in visit_check:
                if i.date_time == date:
                    messages.error(request, _("This time is already token. Select another please."))
                    return HttpResponseRedirect(request.path_info)
            dep = Department.objects.filter(title=department).first()
            department_ID = dep.id
            if request.user.is_patient:
                try:
                    patient = request.user
                    pat = User.objects.filter(username=patient).first()
                    patient_ID = pat.id
                    Appointment.objects.create(patient_ID_id=patient_ID, doctor_ID_id=doc.user_id, date_time=date, department_id=department_ID)
                    messages.success(request, _("Your new appointment is created!"))
                except Exception:
                    messages.error(request, _("The fields must be filled."))
            elif request.user.is_doctor:
                try:
                    patient = request.POST['patient']
                    pat = Patient.objects.filter(name=patient).first()
                    patient_ID = pat.user_id
                    Appointment.objects.create(patient_ID_id=patient_ID, doctor_ID_id=doc.user_id, date_time=date, department_id=department_ID)
                    messages.success(request, _("New appointment is created!"))
                except Exception:
                    messages.error(request, _("The fields must be filled."))
            return redirect('index')
    except Exception:
        messages.error(request, _("The fields must be filled."))

    doctors = Doctor.objects.filter(department__title__in=[department]).all()
    patients = Patient.objects.all()
    context = {
        'doctor': doctors,
        'patient': patients
    }
    return render(request, 'appointment_create.html', context=context)


class PatientRegister(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'patient_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class DoctorRegister(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'doctor_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class PatientVisitsListView(LoginRequiredMixin, ListView):
    model = Appointment
    paginate_by = 10
    context_object_name = 'visit'
    template_name = 'patient_visits_ListView.html'

    def get_queryset(self):
        return Appointment.objects.filter(patient_ID_id=self.request.user.pk).filter(status='w').order_by('-date_time').all()


@login_required
def patient_card(request, pk):
    patient = Patient.objects.filter(user_id=pk).all()
    paginator = Paginator(PatientCard.objects.filter(patient_ID_id=pk).order_by('-appointment_ID_id__date_time').all(), 10)
    page_number = request.GET.get('page')
    card = paginator.get_page(page_number)
    context = {
        'patients': patient,
        'cards': card,
    }
    return render(request, 'patient_card_ListView.html', context=context)


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_listview.html'

    def get_queryset(self):
        return Doctor.objects.order_by('name')


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    paginate_by = 10
    template_name = 'patient_listview.html'

    def get_queryset(self):
        return Patient.objects.order_by('name')


class ServicesListView(ListView):
    model: Service
    template_name = 'services_listview.html'

    def get_queryset(self):
        return Service.objects.order_by('title')


def contact(request):
    return render(request, 'contact.html')


@login_required
def patient_card_detail(request, pk):
    card = PatientCard.objects.filter(id=pk).first()
    context = {
        'card': card
    }
    return render(request, "visit_detailview.html", context=context)


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    paginate_by = 10
    context_object_name = 'visits'

    template_name = 'appointment_listview.html'

    def get_queryset(self):
        return Appointment.objects.filter(doctor_ID_id=self.request.user.id).objects.order_by('date_time').all()


@login_required
def appointment_list(request):
    paginator = Paginator(Appointment.objects.filter(doctor_ID=request.user.id).order_by('-date_time').all(), 10)
    page_number = request.GET.get('page')
    visits = paginator.get_page(page_number)

    context = {
        'visits': visits
    }
    return render(request, 'appointment_listview.html', context=context)


@login_required
def patientcard_create_view(request, pk):
    visits = Appointment.objects.filter(id=pk).first()
    date = visits.date_time
    if request.method == 'POST':
        select_status = request.POST['customRadio']
        if select_status == 'c':
            symptoms = request.POST['symptoms']
            treatment = request.POST['treatment']
            prognosis = request.POST['prognosis']
            comments = request.POST['comments']
            doctor_ID = request.user.pk
            appointment_ID = pk
            patient = Appointment.objects.filter(id=pk).first()
            patient_ID = patient.patient_ID.user_id
            PatientCard.objects.create(symptoms=symptoms, treatment=treatment, prognosis=prognosis, comments=comments, doctor_ID_id=doctor_ID, appointment_ID_id=appointment_ID,
                                       patient_ID_id=patient_ID)
            messages.success(request, _("The new record is created and Invoice is sent to patient email!"))
            invoice_lines = request.POST.getlist('services')
            send_invoice(patient_ID, date, invoice_lines)
            visits.status = request.POST['customRadio']
            visits.save()
            return redirect('index')
        elif select_status == 'x':
            visits.status = select_status
            visits.save()
            return redirect('visits')
    services = Service.objects.order_by('title').all()
    context = {
        'visits': visits,
        'services': services
    }
    return render(request, 'patientCard_createview.html', context=context)


def send_mail(email, bodyContent):
    to_email = email
    from_email = EMAIL_HOST_USER
    subject = _('Thank you for coming to Cleveland Clinic!')
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    message.attach(MIMEText(bodyContent, "html"))
    msgBody = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, EMAIL_HOST_PASSWORD)
    server.sendmail(from_email, to_email, msgBody)

    server.quit()


def send_invoice(patient_ID, date, invoice_lines):
    services_list = []
    for service in invoice_lines:
        item = Service.objects.filter(id=service).first()
        services_list.append(item)
    create_invoice(patient_ID, date, services_list)
    patient = Patient.objects.filter(user_id=patient_ID).first()
    invoice = Invoice.objects.latest('id')

    template = env.get_template('invoice.html')
    output = template.render(data=services_list, invoice=invoice, patient=patient)
    send_mail(patient.email, output)
    return _("Mail sent successfully.")


def create_invoice(patient_ID, date, services_list):
    new_invoice = Invoice.objects.create(date=date, patient_ID_id=patient_ID)
    invoice_id = new_invoice.id
    for service in services_list:
        InvoiceLine.objects.create(price=service.price, service_ID_id=service.id, invoice_ID_id=invoice_id)
    PatientCard.objects.filter(patient_ID=patient_ID).filter(appointment_ID__date_time=date).update(invoice_ID=invoice_id)
    return _("Invoice %(invoice_id)s was successfully created.") % {'invoice_id':invoice_id}


@login_required
def invoice_list_view(request):
    paginator = Paginator(Invoice.objects.filter(patient_ID=request.user.id).order_by('-date').all(), 10)
    page_number = request.GET.get('page')
    invoices = paginator.get_page(page_number)
    context = {
        'invoices': invoices,
    }
    return render(request, 'invoices_listview.html', context=context)


@login_required
def invoice_detail_view(request, id):
    invoices = Invoice.objects.filter(id=id).first()
    invoice_lines = InvoiceLine.objects.filter(invoice_ID=id).all()
    context = {
        'invoice': invoices,
        'invoice_lines': invoice_lines
    }
    return render(request, 'InvoiceLine_detailview.html', context=context)


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,_("Profile is now updated!"))
            return redirect('profilis')
        else:
            messages.error(
                request, (_('There was an error updating your profile')))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


@login_required
def doctor_profile_edit(request):
    user = request.user
    form = DoctorUpdateForm(request.POST or None, initial={'user_id': user}, instance=request.user.doctor)
    doctor = Doctor.objects.filter(user_id=user).first()

    if request.method == 'POST':
        if form.is_valid():
            doctor.name = request.POST['name']
            doctor.phone_number = request.POST['phone_number']
            doctor.experience = request.POST['experience']
            doctor.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        "form": form,
        "doctor": doctor
    }

    return render(request, "doctor_form.html", context)


@login_required
def patient_profile_edit(request):
    user = request.user
    form = PatientUpdateForm(request.POST or None, initial={'user_id': user}, instance=request.user.patient)
    patient = Patient.objects.filter(user_id=user).first()

    if request.method == 'POST':
        if form.is_valid():
            patient.name = request.POST['name']
            patient.phone_number = request.POST['phone_number']
            patient.birth_day = request.POST['birth_day']
            patient.address = request.POST['address']
            patient.SD = request.POST['SD']
            patient.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        "form": form,
        "patient": patient
    }

    return render(request, "patient_form.html", context)

@login_required
def patient_card_edit(request, pk):
    user = request.user
    patientcard = PatientCard.objects.filter(id=pk).first()
    appointment = Appointment.objects.filter(patientcard=pk).first()
    form = PatientCardUpdateForm(request.POST or None, instance=patientcard)
    if request.method == 'POST':
        if user.id == patientcard.doctor_ID.user_id:
            patientcard.symptoms = request.POST['symptoms']
            patientcard.treatment = request.POST['treatment']
            patientcard.prognosis = request.POST['prognosis']
            patientcard.comments = request.POST['comments']
            appointment.status = request.POST['customRadio']
            patientcard.save()
            appointment.save()
            return redirect(f'/appointment/{pk}')
        else:
            messages.warning(request, _("Sorry you do not have permission!"))
    context = {
        "form": form,
        "patientcard": patientcard
    }
    return render(request, "patientCard_createview_update.html", context)


def search(request):
    query = request.GET.get('query')
    search_results = Patient.objects.filter(Q(name__icontains=query) | Q(email__icontains=query))
    return render(request, 'search.html', {'patients': search_results, 'query': query})
