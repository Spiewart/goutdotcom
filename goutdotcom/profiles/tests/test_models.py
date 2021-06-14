import pytest

from .factories import PatientProfileFactory

pytestmark = pytest.mark.django_db

class TestUrateMethods:
    def test__str__(self):
        urate = UrateFactory()
        assert(urate.__str__() == str(urate.uric_acid))

    def test__unicode__(self):
        urate = UrateFactory()
        assert(urate.__unicode__() == str(urate.name))

    def test_get_absolute_url(self):
        urate = UrateFactory()
        assert urate.get_absolute_url() == f"/lab/urate/{urate.pk}/"