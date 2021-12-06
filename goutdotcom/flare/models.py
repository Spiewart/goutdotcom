from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import format_lazy
from django_extensions.db.models import TimeStampedModel
from multiselectfield import MultiSelectField

from ..history.models import CHF, PVD, HeartAttack, Hypertension, Stroke
from ..lab.models import Urate
from .choices import *


class Flare(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    monoarticular = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Monoarticular",
        help_text="Does your gout flare involve only 1 joint?",
        default=False,
        null=True,
        blank=True,
    )

    male = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Male?",
        help_text="Are you male (biologically from birth or medically after birth)?",
        default=False,
        null=True,
        blank=True,
    )

    prior_gout = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Prior Gout Flare",
        help_text=format_lazy(
            """Have you had a prior <a href='{}' target='_blank'>gout flare</a>or other sudden onset arthritis attack consistent with gout?""",
            reverse_lazy("flare:about"),
        ),
        default=False,
        null=True,
        blank=True,
    )

    onset = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Rapid Onset (1 day)",
        help_text="Did your symptoms start and reach maximum intensity within 1 day?",
        default=False,
        null=True,
        blank=True,
    )

    redness = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Redness",
        help_text="Is(are) the joint(s) red (erythematous)?",
        default=False,
        null=True,
        blank=True,
    )

    firstmtp = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Is your big toe the painful joint?",
        help_text="Is the ",
        default=False,
        null=True,
        blank=True,
    )

    location = MultiSelectField(
        choices=LIMITED_JOINT_CHOICES, blank=True, null=True, help_text="What joint did the flare occur in?"
    )

    cardiacdisease = models.BooleanField(
        choices=BOOL_CHOICES,
        blank=True,
        null=True,
        default=False,
        help_text="Do you have a history of hypertension or cardiac disease(s)?",
        verbose_name="Cardiac disease or equivalents",
    )

    hypertension = models.ForeignKey(
        Hypertension,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    heartattack = models.ForeignKey(
        HeartAttack,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    CHF = models.ForeignKey(
        CHF,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    stroke = models.ForeignKey(
        Stroke,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    PVD = models.ForeignKey(
        PVD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    urate = models.OneToOneField(
        Urate,
        on_delete=models.CASCADE,
        help_text="Did you get your uric acid checked at the time of your flare?",
        blank=True,
        null=True,
    )

    duration = models.IntegerField(null=True, blank=True, help_text="How long did it last? (days)")

    treatment = MultiSelectField(
        choices=TREATMENT_CHOICES, blank=True, null=True, help_text="What was the flare treated with?"
    )

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{(str(self.user), str(self.location))}"

    def get_absolute_url(self):
        return reverse("flare:detail", kwargs={"pk": self.pk})

    def flare_calculator(self):
        unlikely = "unlikely"
        equivocal = "equivocal"
        likely = "likely"

        points = 0

        if self.male == True:
            points = points + 2
        if self.prior_gout == True:
            points = points + 2
        if self.onset == True:
            points = points + 0.5
        if self.redness == True:
            points = points + 1
        if self.firstmtp == True:
            points = points + 2.5
        if (
            self.cardiacdisease != None
            or self.hypertension.value == True
            or self.heartattack.value == True
            or self.CHF.value == True
            or self.stroke.value == True
            or self.PVD.value == True
        ):
            points = points + 1.5
        if self.urate.value >= 6.0:
            points = points + 3.5

        if points < 4:
            return unlikely
        if points >= 4 and points < 8:
            return equivocal
        if points > 8:
            return likely
