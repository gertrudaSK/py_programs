from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Doctor, Patient, Appointment, Department, Profile, PatientCard


class PatientSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    birth_day = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)
    SD = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'User', }), label=u'Social Insurance ID',
        max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user=user)
        patient.name = self.cleaned_data.get('name')
        patient.phone_number = self.cleaned_data.get('phone_number')
        patient.address = self.cleaned_data.get('address')
        patient.birth_day = self.cleaned_data.get('birth_day')
        patient.email = self.cleaned_data.get('email')
        patient.SD = self.cleaned_data.get('SD')
        patient.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.CharField(required=True)
    experience = forms.CharField(required=True)
    department = forms.CharField(required=True)

    def save(self, commit=True):
        user = super(DoctorSignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.phone_number = self.cleaned_data.get('phone_number')
        doctor.designation = self.cleaned_data.get('designation')
        doctor.save()
        return user


class AppointmentDepartmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('department',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'phone_number', 'experience', 'department']


class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'birth_day', 'phone_number', 'address', 'SD']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nuotrauka']

class PatientCardUpdateForm(forms.ModelForm):
    symptoms = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'PatientCard', }), label=u'Symptoms',
        max_length=1000, required=True)
    treatment = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'PatientCard', }), label=u'Treatment',
        max_length=1000, required=True)
    prognosis = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'PatientCard', }), label=u'Prognosis',
        max_length=1000, required=True)
    comments = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'PatientCard', }), label=u'Comments',
        max_length=1000, required=True)

    class Meta:
        model = PatientCard
        fields = '__all__'
