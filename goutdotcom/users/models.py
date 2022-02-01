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

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    role = models.CharField(_("Role"), max_length=50, choices=Roles.choices)

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
        proxy = True

    # Custom methods for Patient Role go here...
    @property
    def extra(self):
        try:
            return self.patientprofile
        except self.patientprofile.DoesNotExist:
            return None


class ProviderManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=User.Roles.PROVIDER)


class Provider(User):
    # This sets the user type to PROVIDER during record creation
    base_role = User.Roles.PROVIDER

    # Ensures queries on the Provider model return only Providers
    objects = ProviderManager()

    # Setting proxy to "True" means a table will not be created for this record
    class Meta:
        proxy = True
        permissions = [
            ("can_add_patient", "Can Add Patient"),
            ("can_edit_patient", "Can Edit Patient"),
            ("can_delete_patient", "Can Delete Patient"),
            ("can_view_patient", "Can View Patient"),
        ]

    # Custom methods for Provider Role go here...
    @property
    def extra(self):
        try:
            return self.providerprofile
        except self.providerprofile.DoesNotExist:
            return None
