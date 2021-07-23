from autoslug import AutoSlugField
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from django.utils.crypto import get_random_string
import datetime

from goutdotcom.users.models import models

# Create your models here.
sexes = (('male', 'male'), ('female', 'female'), ('non-binary', 'non-binary'))
races = (('white', 'white'), ('black', 'black'), ('asian', 'asian'), ('native american', 'native american'), ('hispanic', 'hispanic'))

class PatientProfile(TimeStampedModel):
    # Default User profile
    # If you do this you need to either have a post_save signal or redirect to a profile_edit view on initial login
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    picture = models.ImageField(default="default_image.jpg", null=True, blank=True, help_text="Upload a picture for your profile")
    bio = models.CharField(max_length=500, help_text="500 character bio", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=sexes, help_text='Enter gender', null=True, blank=True, default='male')
    race = models.CharField(max_length=40, choices=races, help_text='Enter race', null=True, blank=True, default='white')
    weight = models.IntegerField(help_text="How much do you weight in pounds?", null=True, blank=True)
    height = models.IntegerField(help_text="How tall are you in feet/inches?", null=True, blank=True)
    drinks_per_week = models.IntegerField(null=True, blank=True)

    def get_age(self):
        if self.date_of_birth:
            age = datetime.date.today().year - self.date_of_birth.year
            return age
        else:
            return "No date of birth recorded"

    def BMI_calculator(self):
        def weight_kgs_calc(self):
            if self.weight != None:
                return self.weight / 2.205
            else:
                return "Enter a weight in pounds"

        def height_meters_calc(self):
            if self.height:
                return self.height / 39.37
            else:
                return "Enter a height in inches"

        if self.weight is not None and self.height is not None:
            BMI = weight_kgs_calc(self) / (height_meters_calc(self) ** 2)
            return BMI
        elif self.weight is None:
            if self.height is None:
                return "Enter a valid height and weight"
            else:
                return weight_kgs_calc(self)
        elif self.height is None:
            if self.weight is None:
                return "Enter a valid height and weight"
            else:
                return height_meters_calc(self)

    def __str__(self):
        return str(self.user.username + "'s profile")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.user_username})

