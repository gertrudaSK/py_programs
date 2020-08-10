from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User, Patient, Doctor, PatientCard, Appointment, Service, InvoiceLine, Invoice, Department, Profile


class UserAdmin(BaseUserAdmin):
    model = User
    list_filter = ('email', 'username',)
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password1', 'password2', 'email', 'is_patient', 'is_doctor')}
         ),
    )
    list_display = ('username', 'email','is_patient', 'is_doctor')

    class Meta:
        model = User


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_day', 'email', 'phone_number', 'address', 'SD', 'balance')
    list_filter = ('email', 'name',)

    class Meta:
        model = Patient


class PatientCardForm(forms.ModelForm):
    class Meta:
        model = PatientCard
        fields = '__all__'
        widgets = {'symptoms': forms.Textarea(),
                   'treatment': forms.Textarea(),
                   'prognosis': forms.Textarea(),
                   'comments': forms.Textarea()
                   }


class PatientCardAdmin(admin.ModelAdmin):
    form = PatientCardForm
    list_filter = ('patient_ID',)
    list_display = ('patient_ID', 'department', 'visit_date', 'status')

    def get_ordering(self, request):
        return ['-appointment_ID']


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'display_departments')
    list_filter = ('email', 'name',)

    class Meta:
        model = Doctor


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('visit_department', 'patient_ID', 'doctor_ID', 'date_and_time')
    list_filter = ('patient_ID', 'doctor_ID',)

    def get_ordering(self, request):
        return ['-date_time']

    class Meta:
        model = Appointment


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')

    class Meta:
        model = Service


class InvoiceLineTabularInline(admin.TabularInline):
    model = InvoiceLine
    can_delete = False


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('date', 'invoice_no', 'patient_ID', 'sum', 'status')

    inlines = [InvoiceLineTabularInline]
    list_filter = ('invoice_no',)

    class Meta:
        model = Invoice


class InvoiceLineAdmin(admin.ModelAdmin):
    list_filter = ('price')
    list_display = ('quantity', 'price', 'rate', 'service_ID', 'invoice_ID')
    autocomplete_fields = ['service_ID']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'doctor_ID')


admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(PatientCard, PatientCardAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Department)
admin.site.register(Profile)
