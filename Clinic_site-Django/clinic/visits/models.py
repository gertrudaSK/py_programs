import datetime

from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    name = models.CharField(max_length=100)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient')
    name = models.CharField(_('name'), max_length=50, null=True)
    birth_day = models.DateField(_('birth day'), null=True)
    email = models.CharField(_('email'), max_length=70, null=True)
    phone_number = models.CharField(_('phone number'), max_length=20, null=True)
    address = models.CharField(_('address'), max_length=200, null=True)
    SD = models.CharField(_('Social Insurance ID'), max_length=10, null=True)

    @property
    def balance(self):
        rows = InvoiceLine.objects.filter(invoice_ID__patient_ID=self.user_id).all()
        sum = 0
        for row in rows:
            sum += row.sum
        return sum

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")


class PatientCard(models.Model):
    patient_ID = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, db_constraint=False)
    doctor_ID = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, db_constraint=False)
    symptoms = models.CharField(_('symptoms'), max_length=5000)
    treatment = models.CharField(_('treatment'), max_length=5000)
    prognosis = models.CharField(_('prognosis'), max_length=1000)
    comments = models.CharField(_('comments'), max_length=5000)
    appointment_ID = models.OneToOneField('Appointment', on_delete=models.CASCADE, related_name='patientcard')
    invoice_ID = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True, db_constraint=False)

    class Meta:
        verbose_name = _("Patient Card Record")
        verbose_name_plural = _("Patient Card Records")

    def __str__(self):
        return self.patient_ID.name

    @property
    def status(self):
        if self.appointment_ID.status == 'w':
            return _("Waiting")
        elif self.appointment_ID.status == 'c':
            return _("Completed")
        elif self.appointment_ID.status == 'x':
            return _("Canceled")

    @property
    def visit_date(self):
        date = str(self.appointment_ID.date_time)
        date_time = date[:16]
        return date_time

    @property
    def department(self):
        return self.appointment_ID.department.title


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor')
    name = models.CharField(_('name'), max_length=50, null=True)
    phone_number = models.CharField(_('phone number'), max_length=20)
    email = models.CharField(_('email'), max_length=70, null=True)
    experience = models.IntegerField(_('experience (years)'), null=True)
    department = models.ManyToManyField('Department',
                                        help_text='Choose the department')

    def display_departments(self):
        return ', '.join(dep.title for dep in self.department.all())

    display_departments.short_description = _('Departments')

    class Meta:
        verbose_name = _('Doctor')
        verbose_name_plural = _('Doctors')

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient_ID = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, related_name='appointment', db_constraint=False)
    doctor_ID = models.ForeignKey('Doctor', null=True, on_delete=models.SET_NULL, related_name='appointment', db_constraint=False)
    date_time = models.DateTimeField(_('appointment date and time'))
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='appointment')
    STATUS = (
        ('w', (_('waiting'))),
        ('c', (_('completed'))),
        ('x', (_('canceled'))),
    )

    status = models.CharField(max_length=1,
                              choices=STATUS,
                              blank=True,
                              default='w',
                              help_text=(_('Status'))
                              )
    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")

    def __str__(self):
        date = str(self.date_time)
        return f"{self.patient_ID.name}, {date}"

    @property
    def visit_department(self):
        return self.department.title

    @property
    def date_and_time(self):
        date = str(self.date_time)
        datetimes = str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        return f"{datetimes}"


class Department(models.Model):
    title = models.CharField(_('Department'), max_length=100)

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(_('service'), max_length=100)
    price = models.FloatField(_('price'))
    department_ID = models.ManyToManyField('Department', help_text='Choose the department')

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f"{self.title}: {self.price} $"


class InvoiceLine(models.Model):
    quantity = models.FloatField(_('Quantity'), default=1)
    price = models.FloatField(_('Price'))
    service_ID = models.ForeignKey('Service', on_delete=models.SET_NULL,
                                   null=True)
    invoice_ID = models.ForeignKey('Invoice', on_delete=models.SET_NULL,
                                   null=True, related_name='invoice_line')
    sum = models.FloatField(verbose_name=_("sum"), null=True, blank=True)

    @property
    def get_sum(self):
        sum = self.quantity * self.price
        return sum

    def save(self, *args, **kwargs):
        self.sum = self.get_sum
        super(InvoiceLine, self).save(*args, **kwargs)

    def __float__(self):
        return self.sum

    def __str__(self):
        return f"{self.service_ID.title}, {self.invoice_ID}"

    class Meta:
        verbose_name = _('Invoice line')
        verbose_name_plural = _('Invoice lines')


def increment_invoice_number():
    last_invoice = Invoice.objects.all().order_by('id').last()
    if not last_invoice:
        return 'CLN1'
    invoice_no = last_invoice.invoice_no
    invoice_int = int(invoice_no.split('CLN')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'CLN' + str(new_invoice_int)
    return new_invoice_no


class Invoice(models.Model):
    invoice_no = models.CharField(_('Invoice ID'), max_length=500, default=increment_invoice_number, null=True, blank=True)
    date = models.DateField(_('Invoice date'))
    patient_ID = models.ForeignKey('Patient', on_delete=models.SET_NULL,
                                   null=True)

    STATUS = (
        ('u', (_('unpaid'))),
        ('p', (_('paid'))),
        ('c', (_('canceled'))),
    )

    status = models.CharField(max_length=1,
                              choices=STATUS,
                              blank=True,
                              default='u',
                              help_text=(_('Status')),
                              )

    @property
    def sum(self):
        rows = InvoiceLine.objects.filter(invoice_ID=self.id)
        sum = 0
        for row in rows:
            sum += row.sum
        return sum

    def __str__(self):
        return f"{self.invoice_no} {self.patient_ID.name} {self.date}"

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['date']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(_('Image'), default="default.png", upload_to="profile_pics")

    def __str__(self):
        if self.user.is_patient:
            return _("%(username)s profile") % {'username': self.user.patient.name}
        elif self.user.is_doctor:
            return _("%(username)s profile") % {'username': self.user.doctor.name}
        else:
            return _("%(username)s profile") % {'username': self.user.username}

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
