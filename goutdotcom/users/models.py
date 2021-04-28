from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Default user for goutdotcom."""
    # User types for different roles
    class Roles(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        PROVIDER = "PROVIDER", "Provider"
        INVENTOR = "ADMINISTRATOR", "Administrator"

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    # Ensures that creating new users through proxy models works
    base_role = Roles.PATIENT

    role = models.CharField(
        _("Role"), max_length=50, choices=Roles.choices, default=Roles.PATIENT
    )

    def save(self, *args, **kwargs):
        # If a new user, set the user's role based off the base_role property
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get url for user's detail view.


        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=User.Roles.PATIENT)

class Patient(User):
    # This sets the user type to PATIENT during record creation
    base_role = User.Roles.PATIENT

    # Ensures queries on the Patient model return only Patients
    objects = PatientManager()

    # Setting proxy to "True" means a table will not be created for this record
    class Meta:
        proxy=True

    # Custom methods for Patient Role go here...
    @property
    def extra(self):
        return self.patientprofile
