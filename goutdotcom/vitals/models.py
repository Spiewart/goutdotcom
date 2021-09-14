from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import NullBooleanField
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from django.utils import timezone

from .choices import *
from math import floor

# Create your models here.
class Vital(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = NullBooleanField()
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True)
    altunit = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True)
    name = "vital"
    date_recorded = models.DateTimeField(help_text="What day was this lab drawn?", default=timezone.now, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse("vitals:detail", kwargs={"pk":self.pk, "vital":self.name})

    def __unicode__(self):
        return self.name

class Weight(Vital):
    value = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(
        600)], help_text="Enter your weight in pounds", null=True, blank=True)
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=POUNDS)
    altunit = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=KILOS)
    name = "weight"

    def convert_pounds_to_kg(self):
        return round(self.value / 2.205, 1)


class Height(Vital):
    value = models.IntegerField(validators=[MinValueValidator(36), MaxValueValidator(
        100)], help_text="Enter your height in inches", null=True, blank=True)
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=INCHES)
    altunit = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=METERS)
    name = "height"

    def convert_inches_to_feet(self):
        feet = floor(self.value / 12)
        inches = self.value - feet * 12
        return str(feet) + " foot " + str(inches) + " inches"

    def convert_inches_to_meters(self):
        return round(self.value / 39.37, 2)
