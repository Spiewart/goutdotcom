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
    ### NEED TO ADD ANGINA TO MEDICAL PROFILE...

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

    duration = models.CharField(
        max_length=60,
        choices=DURATION_CHOICES,
        verbose_name="Symptom Duration",
        help_text="How long did your symptoms last?",
        null=True,
        blank=True,
    )

    treatment = MultiSelectField(
        choices=TREATMENT_CHOICES, blank=True, null=True, help_text="What was the flare treated with?"
    )

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{(str(self.user), str(self.location))}"

    def get_absolute_url(self):
        return reverse("flare:detail", kwargs={"pk": self.pk})

    def locations(self):
        """Function that evaluates monoarticular, firstmtp, and location fields and returns a string describing the location(s) of the flare

        returns: [str]: [str describing the location(s) of the flare]"""

        location_string = ""

        if self.monoarticular:
            if self.monoarticular == True:
                location_string += "monoarticular"
                if self.firstmtp:
                    if self.firstmtp == True:
                        location_string += ", big toe"
                else:
                    if len(self.location) > 0:
                        if len(self.location) == 1:
                            location_string += ", " + self.location[0]
                        else:
                            location_string += ", "
                            for i in range(len(self.location) - 1):
                                location_string += self.location[i] + ", "
                            location_string += self.location[len(self.location) - 1]
        else:
            location_string += "polyarticular"
            if len(self.location) > 0:
                location_string += ", "
                if len(self.location) == 1:
                    if self.firstmtp:
                        if self.firstmtp == True:
                            location_string += "big toe, "
                    location_string += self.location[0]
                else:
                    if self.firstmtp:
                        if self.firstmtp == True:
                            location_string += "big toe, "
                    for i in range(len(self.location) - 1):
                        location_string += self.location[i] + ", "
                    location_string += self.location[len(self.location) - 1]
            else:
                if self.firstmtp:
                    if self.firstmtp == True:
                        location_string += ", big toe"
        return location_string.lower()

    def flare_calculator(self):
        """Function to take user-generated input from Flare and returns a prevalence of gout based on evidence from a 2 center European study.
        Offers recommendation on who benefits from synovial fluid analysis vs who is unlikely to have gout and who is very likely to have gout.

        Returns:
                    [dict]: [dict with keys to calculator result, likelihood of gout, prevalence of gout in similar patient populations, and a caveat that this can't be applied to non-monoarticular flares if the flare was submitted as not monoarticular.]

        Citations:
        1. Janssens HJEM, Fransen J, van de Lisdonk EH, van Riel PLCM, van Weel C, Janssen M. A Diagnostic Rule for Acute Gouty Arthritis in Primary Care Without Joint Fluid Analysis. Arch Intern Med. 2010;170(13):1120–1126. doi:10.1001/archinternmed.2010.196
        2. Laura B. E. Kienhorst, Hein J. E. M. Janssens, Jaap Fransen, Matthijs Janssen, The validation of a diagnostic rule for gout without joint fluid analysis: a prospective study, Rheumatology, Volume 54, Issue 4, April 2015, Pages 609–614, https://doi.org/10.1093/rheumatology/keu378
        """

        calc_package = {"result": "no data", "likelihood": "unknown", "prevalence": "unknown", "caveat": None}

        unlikely = "unlikely"
        equivocal = "equivocal"
        likely = "likely"

        lowrange = "Gout is not likely and alternative causes of symptoms should be investigated."
        midrange = "Indeterminate likelihood of gout and it can't be ruled in or out. Physician evaluation is required."
        highrange = "Gout is very likely. Not a whole lot else needs to be done, other than treat your gout!"

        lowprev = "2.2%"
        modprev = "31.2%"
        highprev = "80.4%"

        points = 0
        cardiac_disease_equivalent = False

        if self.monoarticular == True:
            calc_package[
                "caveat"
            ] = "This calculator has only been validated for monoarticular (1 joint) flares. It can't necessarily be applied to polyarticular (more than 1 joint) flares."

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
        if cardiac_disease_equivalent == False:
            if self.hypertension:
                if self.hypertension.value == True:
                    cardiac_disease_equivalent = True
            if self.hypertension:
                if self.heartattack.value == True:
                    cardiac_disease_equivalent = True
            if self.CHF:
                if self.CHF.value == True:
                    cardiac_disease_equivalent = True
            if self.stroke:
                if self.stroke.value == True:
                    cardiac_disease_equivalent = True
            if self.PVD:
                if self.PVD.value == True:
                    cardiac_disease_equivalent = True

        if cardiac_disease_equivalent == True:
            points = points + 1.5

        if self.urate:
            if self.urate.value >= 6.0:
                points = points + 3.5

        if points < 4:
            calc_package["result"] = unlikely
            calc_package["likelihood"] = lowrange
            calc_package["prevalence"] = lowprev
        if points >= 4 and points < 8:
            calc_package["result"] = equivocal
            calc_package["likelihood"] = midrange
            calc_package["prevalence"] = modprev
        if points > 8:
            calc_package["result"] = likely
            calc_package["likelihood"] = highrange
            calc_package["prevalence"] = highprev

        return calc_package
