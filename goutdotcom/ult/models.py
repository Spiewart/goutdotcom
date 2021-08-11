from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse

# Create your models here.
class ULT(TimeStampedModel):
    ZERO = 'zero'
    ONE = 'one'
    FEW = '1-3'
    LOTS = '4-6'
    CONSTANT = '7 or more'

    UNDER_TWO = 'Under two'
    GREATER_TWO = 'Two or more'

    ULT_CHOICES = (
        (ZERO, 'Zero'),
        (ONE, 'One'),
        (FEW, '2-3'),
        (LOTS, '4-6'),
        (CONSTANT, '7 or more'),
    )

    FREQ_CHOICES = (
        (UNDER_TWO, 'Under two'),
        (GREATER_TWO, 'Two or more'),
    )

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    first_flare = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Are you having your first flare?", help_text="If so, disregard the rest of the questions.")
    num_flares = models.CharField(max_length=30, choices=ULT_CHOICES, verbose_name="Approximately how many gout flares have you had?",
                                  help_text="An estimate is fine!", default=ONE)
    freq_flares = models.CharField(max_length=30, choices=FREQ_CHOICES, verbose_name="Approximately how many flares do you have per year?",
                                   help_text="An estimate is fine!", default=UNDER_TWO)
    erosions = models.BooleanField(
        choices=BOOL_CHOICES, verbose_name="Do you have erosions on your x-rays?", help_text="If you don't know, that's OK!", default=False)
    tophi = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Do you have tophi?", help_text="If you don't know, that's OK!", default=False)
    stones = models.BooleanField(
        choices=BOOL_CHOICES, verbose_name="Have you ever had kidney stones made of uric acid?", help_text="If you don't know, that's OK!", default=False)
    ckd = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Do you have chronic kidney disease (CKD) stage III or greater?",
                              help_text="If you don't know, that's OK!", default=False)
    uric_acid = models.BooleanField(
        choices=BOOL_CHOICES, verbose_name="Is your uric acid over 9.0?", help_text="If you don't know, that's OK!", default=False)

    def calculator(self):
        go_forth = "Urate lowering therapy is recommended for your gout."
        abstain = "Urate lowering therapy isn't indicated for your gout."
        conditional = "Urate lowering therapy is conditionally recommended for your gout."

        if self.first_flare == True or self.num_flares == "One":
            if self.erosions == True or self.tophi == True:
                return go_forth
            elif self.ckd == True or self.uric_acid == True or self.stones == True:
                return conditional
            else:
                return abstain
        if self.num_flares == "Zero":
            if self.erosions == True or self.tophi == True:
                return go_forth
            else:
                return abstain
        if self.freq_flares == "Two or more":
            return go_forth
        if self.freq_flares == "Under two":
            if self.erosions == True or self.tophi == True:
                return go_forth
            elif self.num_flares != "Zero" or "One":
                return conditional
        else:
            return abstain

    def __str__(self):
        return self.calculator()

    def get_absolute_url(self):
        return reverse("ult:detail", kwargs={"pk":self.pk})
