import pytest

from goutdotcom.users.models import User
from goutdotcom.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass