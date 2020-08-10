from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointment/new/', views.select_department, name='appointment'),
    path('appointment/history/', views.PatientVisitsListView.as_view(), name='appointment-active'),
    path('patientcard/<int:pk>/', views.patient_card, name='patient-card'),
    path('appointment/new/<department>/', views.new_appointment, name='new-appointment'),
    path('patient_register/', views.PatientRegister.as_view(), name='patient_register'),
    path('doctor_register/', views.DoctorRegister.as_view(), name='doctor_register'),
    path('doctors/', views.DoctorListView.as_view(), name='doctors_list'),
    path('appointment/<int:pk>', views.patient_card_detail, name='visit-detail'),
    path('appointment/<int:pk>/update', views.patient_card_edit, name='visit-update'),
    path('patients/', views.PatientListView.as_view(), name='patients_list'),
    path('appointments/', views.appointment_list, name='visits'),
    path('appointment/<int:pk>/new-card-record', views.patientcard_create_view, name='new-card-record'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.ServicesListView.as_view(), name='services'),
    path('invoice/', views.invoice_list_view, name='invoices'),
    path('invoice/<int:id>/', views.invoice_detail_view, name='invoice-detail'),
    path('profile/', views.profile, name='profilis'),
    path('profile/update/', views.doctor_profile_edit, name='doctor-update'),
    path('profile/patient-update/', views.patient_profile_edit, name='patient-update'),
    path('search/', views.search, name='search'),
    path(r'^i18n/', include('django.conf.urls.i18n')),
]
