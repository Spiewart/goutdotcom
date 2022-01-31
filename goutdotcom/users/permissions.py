from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Patient

content_type = ContentType.objects.get_for_model(Patient, for_concrete_model=False)
permission = Permission.objects.create(
    codename='can_create_patient',
    name='Can Create Patient',
    content_type=content_type,
)
permission = Permission.objects.create(
    codename='can_edit_patient',
    name='Can Edit Patient',
    content_type=content_type,
)
