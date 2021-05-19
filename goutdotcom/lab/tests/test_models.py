import pytest
from django.test import TestCase

from ..models import Urate, ALT, AST, Platelet, WBC, Hemoglobin, Creatinine
from .factories import UrateFactory

pytestmark = pytest.mark.django_db

class UrateTests(TestCase):
    def test__str__(self):
        urate = UrateFactory()
        
        assert(urate.__str__() == str(urate.uric_acid))

    def test_urate_get_absolute_url(urate:Urate):
        assert urate.get_absolute_url() == f"/urate/{urate.pk}/"
        