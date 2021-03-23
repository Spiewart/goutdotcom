from django.conf import settings
from django.db import models

from goutdotcom.users.models import models

# Create your models here.
class PatientProfile(models.Model):
    # Default User profile
    # If you do this you need to either have a post_save signal or redirect to a profile_edit view on initial login
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    picture = models.ImageField(default="default_image.jpg", null=True, blank=True)

