from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from .choices import *
from ..history.models import CKD, Erosions, UrateKidneyStones, Tophi

# Create your models here.
class ULT(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    num_flares = models.CharField(
        max_length=30,
        choices=ULT_CHOICES,
        verbose_name="How many gout flares have you had?",
        help_text="If more than one, an estimate is fine!",
        default="",
        null=True,
        blank=True,
    )
    freq_flares = models.CharField(
        max_length=30,
        choices=FREQ_CHOICES,
        verbose_name="Approximately how many flares do you have per year?",
        help_text="An estimate is fine!",
        default=ONE,
        null=True,
        blank=True,
    )
    erosions = models.ForeignKey(
        Erosions,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    tophi = models.ForeignKey(
        Tophi,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    stones = models.ForeignKey(
        UrateKidneyStones,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ckd = models.ForeignKey(
        CKD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    uric_acid = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Is your uric acid over 9.0?",
        help_text="If you don't know, that's OK!",
        default=False,
        null=True,
        blank=True,
    )

    def calculator(self):
        go_forth = "Indicated"
        abstain = "Not Indicated"
        conditional = "Conditional"

        if self.num_flares == "one":
            if self.erosions.value == True or self.tophi.value == True:
                return go_forth
            elif self.ckd.value == True or self.uric_acid == True or self.stones.value == True:
                return conditional
            else:
                return abstain
        if self.num_flares == "zero":
            if self.erosions.value == True or self.tophi.value == True:
                return go_forth
            else:
                return abstain
        if self.freq_flares == "two or more":
            return go_forth
        if self.freq_flares == "one":
            if self.erosions.value == True or self.tophi.value == True:
                return go_forth
            elif self.num_flares != "zero" or "one":
                return conditional
        else:
            return abstain

    def __str__(self):
        return self.calculator()

    def get_absolute_url(self):
        return reverse("ult:detail", kwargs={"pk": self.pk})
