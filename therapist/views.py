from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.permissions import IsAuthenticated

class DoctorListView(generics.ListAPIView):
    """
    API view to retrieve a list of therapists (doctors) with pagination.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
