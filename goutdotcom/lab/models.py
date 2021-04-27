from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from decimal import *

# Create your models here.
def unlogged_user():
    return get_user_model().objects.get_or_create(username='unlogged')[0]

class Lab(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Urate(Lab):
    uric_acid = models.DecimalField(max_digits=3, decimal_places=1, help_text="Enter the uric acid")
    name = "Urate"

    def __str__(self):
        return str(self.uric_acid)

    def get_absolute_url(self):
        return reverse("lab:urate-detail", kwargs={"pk":self.pk})

class ALT(Lab):
    alt_sgpt = models.IntegerField(help_text="ALT / SGPT")
    name = "ALT"

    def __str__(self):
        return str(self.alt_sgpt)

    def get_absolute_url(self):
        return reverse("lab:ALT-detail", kwargs={"pk":self.pk})

class AST(Lab):
    ast_sgot = models.IntegerField(help_text="AST / SGOT")
    name = "AST"

    def __str__(self):
        return str(self.ast_sgot)

    def get_absolute_url(self):
        return reverse("lab:AST-detail", kwargs={"pk":self.pk})

class Platelet(Lab):
    platelets = models.IntegerField(help_text="PLT / platelets")
    name = "platelet"

    def __str__(self):
        return str(self.platelets)

    def get_absolute_url(self):
        return reverse("lab:platelet-detail", kwargs={"pk":self.pk})

class WBC(Lab):
    white_blood_cells = models.DecimalField(max_digits=3, decimal_places=1, help_text="WBC")
    name = "WBC"

    def __str__(self):
        return str(self.white_blood_cells)

    def get_absolute_url(self):
        return reverse("lab:WBC-detail", kwargs={"pk":self.pk})

class Hemoglobin(Lab):
    hemoglobin = models.DecimalField(max_digits=3, decimal_places=1, help_text="HGB")
    name = "hemoglobin"

    def __str__(self):
        return str(self.hemoglobin)

    def get_absolute_url(self):
        return reverse("lab:hemoglobin-detail", kwargs={"pk":self.pk})

class Creatinine(Lab):
    creatinine = models.DecimalField(max_digits=4, decimal_places=2, help_text="creatinine")
    name = "creatinine"

    def eGFR_calculator(self):
        kappa = 0
        alpha = 0

        def sex_vars_kappa(self):
            if self.user.patientprofile.gender == 'male':
                return Decimal(0.9)
            elif self.user.patientprofile.gender == 'female':
                return Decimal(0.7)
            else:
                return "Can't calculate eGFR without biologic gender."

        def sex_vars_alpha(self):
            if self.user.patientprofile.gender == 'male':
                return Decimal(float(-0.411))
            elif self.user.patientprofile.gender == 'female':
                return Decimal(-0.329)
            else:
                return "Can't calculate eGFR without biologic gender."

        kappa = sex_vars_kappa(self)
        alpha = sex_vars_alpha(self)

        def race_modifier(self):
            if self.user.patientprofile.race == 'black':
                return Decimal(1.159)
            elif self.user.patientprofile.race == False:
                return "Race is needed to calculate eGFR."
            else:
                return Decimal(1.00)

        def sex_modifier(self):
            if self.user.patientprofile.gender == 'female':
                return Decimal(1.018)
            elif self.user.patientprofile.gender == 'female':
                return Decimal(1.00)
            else: 
                return "Biological gender is needed to calculate eGFR."

        if race_modifier(self).type() == Decimal & sex_modifier(self).type() == Decimal):
            race_modifier(self)
            sex_modifier(self)
            eGFR = Decimal(141) * min(self.creatinine / kappa, Decimal(1.00)) * max(self.creatinine / kappa, Decimal(1.00)) ** Decimal(-1.209) * Decimal(0.993) ** self.user.patientprofile.age ** race_modifier(self) ** sex_modifier(self)
            return eGFR
        else: 
            return "Something went wrong with eGFR calculation"

    def __str__(self):
        return (str(self.creatinine) + " " + str(self.created) + " " + "GFR: " + str(self.eGFR_calculator()))

    def get_absolute_url(self):
        return reverse("lab:creatinine-detail", kwargs={"pk":self.pk})