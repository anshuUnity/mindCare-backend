from django.urls import path
from .views import DoctorListView

urlpatterns = [
    path('therapists/', DoctorListView.as_view(), name='therapist-list'),
]