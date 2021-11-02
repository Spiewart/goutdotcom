from decimal import *

import pytest

from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory

from .factories import ULTAidFactory

pytestmark = pytest.mark.django_db


class TestULTAidMethods:
    def test_get_absolute_url(self):
        ULTAid = ULTAidFactory()
        assert ULTAid.get_absolute_url() == f"/ultaid/{ULTAid.pk}/"

    def test_decision_aid(self):
        ULTAid = ULTAidFactory()
        pass
