import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import json

class Doctor(models.Model):
    """
    A model representing a doctor with various attributes including availability and rating.
    """
    name = models.CharField(_("Name"), max_length=255)
    specialization = models.CharField(_("Specialization"), max_length=255)
    bio = models.TextField(_("Bio"))
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='doctor_pictures/')
    availability = models.TextField(_("Availability"))  # Stores JSON data as a string
    rating = models.DecimalField(
        _("Rating"), max_digits=3, decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
        db_table = 'doctor'

    def get_availability(self):
        """
        Parse the JSON availability field into a Python dictionary.
        """
        return json.loads(self.availability)

    def set_availability(self, availability_dict):
        """
        Convert a Python dictionary to a JSON string and store it in the availability field.
        """
        self.availability = json.dumps(availability_dict)
