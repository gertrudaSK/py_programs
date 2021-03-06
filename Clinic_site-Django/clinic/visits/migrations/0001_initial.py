# Generated by Django 3.0.7 on 2020-06-25 10:53

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import visits.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_patient', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Department')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(blank=True, default=visits.models.increment_invoice_number, max_length=500, null=True, verbose_name='Invoice ID')),
                ('date', models.DateField(verbose_name='Invoice date')),
                ('status', models.CharField(blank=True, choices=[('u', 'unpaid'), ('p', 'paid'), ('c', 'canceled')], default='u', help_text='Status', max_length=1)),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=50, null=True, verbose_name='name')),
                ('phone_number', models.CharField(max_length=20, verbose_name='phone number')),
                ('email', models.CharField(max_length=70, null=True, verbose_name='email')),
                ('experience', models.IntegerField(null=True, verbose_name='experience (years)')),
                ('department', models.ManyToManyField(help_text='Choose the department', to='visits.Department')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=50, null=True, verbose_name='name')),
                ('birth_day', models.DateField(null=True, verbose_name='birth day')),
                ('email', models.CharField(max_length=70, null=True, verbose_name='email')),
                ('phone_number', models.CharField(max_length=20, null=True, verbose_name='phone number')),
                ('address', models.CharField(max_length=20, null=True, verbose_name='address')),
                ('SD', models.CharField(max_length=10, null=True, verbose_name='Social Insurance ID')),
            ],
            options={
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patients',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='service')),
                ('price', models.FloatField(verbose_name='price')),
                ('department_ID', models.ManyToManyField(help_text='Choose the department', to='visits.Department')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuotrauka', models.ImageField(default='default.png', upload_to='profile_pics', verbose_name='Image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=1, verbose_name='Quantity')),
                ('price', models.FloatField(verbose_name='Price')),
                ('sum', models.FloatField(blank=True, null=True, verbose_name='sum')),
                ('invoice_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_line', to='visits.Invoice')),
                ('service_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='visits.Service')),
            ],
            options={
                'verbose_name': 'Invoice line',
                'verbose_name_plural': 'Invoice lines',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='appointment date and time')),
                ('status', models.CharField(blank=True, choices=[('w', 'waiting'), ('c', 'completed'), ('x', 'canceled')], default='w', help_text='Status', max_length=1)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointment', to='visits.Department')),
                ('doctor_ID', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointment', to='visits.Doctor')),
                ('patient_ID', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointment', to='visits.Patient')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
            },
        ),
        migrations.CreateModel(
            name='PatientCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptoms', models.CharField(max_length=5000, verbose_name='symptoms')),
                ('treatment', models.CharField(max_length=5000, verbose_name='treatment')),
                ('prognosis', models.CharField(max_length=1000, verbose_name='prognosis')),
                ('comments', models.CharField(max_length=5000, verbose_name='comments')),
                ('appointment_ID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patientcard', to='visits.Appointment')),
                ('invoice_ID', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='visits.Invoice')),
                ('doctor_ID', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='visits.Doctor')),
                ('patient_ID', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='visits.Patient')),
            ],
            options={
                'verbose_name': 'Patient Card Record',
                'verbose_name_plural': 'Patient Card Records',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='patient_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='visits.Patient'),
        ),
    ]
