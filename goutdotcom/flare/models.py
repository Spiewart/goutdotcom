from autoslug import AutoSlugField
from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
"""
class Flare(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    slug = AutoSlugField(
            "Flare Detail", unique=True, always_update=False, populate_from="created_at"
        )

    joints = (('Toe', 'Toe'), ('Ankle', 'Ankle'), ('Knee', 'Knee'), ('Hip', 'Hip'), ('Finger', 'Finger'), ('Wrist', 'Wrist'), ('Elbow','Elbow'), ('Shoulder', 'Shoulder'))
    location = models.CharField(max_length=8, choices=joints, default='Toe', help_text="What joint did the flare occur in?")

    treatments = (('NSAID', 'NSAID'), ('colchicine', 'colchicine'), ('PO steroid', 'PO steroid'), ('INJ steroid', 'INJ steroid'), ('Tincture of time', 'Tincture of time'))
    treated_with = models.CharField(max_length=20, choices=treatments, default='NSAID', help_text="What was the flare treated with?")

    duration = models.IntegerField(help_text="How long did it last? (days)")
    urate = models.OneToOneField('Urate', on_delete=models.CASCADE, help_text="What was the uric acid at the time of the flare?", blank=True, null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{(str(self.date), str(self.user), str(self.location))}'

    def get_absolute_url(self):
        return reverse('flare:detail', args=[str(self.created)])"""