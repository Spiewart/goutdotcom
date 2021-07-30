import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_create():
    assert (
        reverse("vitals:create", kwargs={"vital": "weight"})
        == f"/vitals/create/weight/"
    )


def test_detail():
    assert (
        reverse("vitals:detail", kwargs={"vital": "weight", "pk":1})
        == f"/vitals/weight/1/"
    )
    assert resolve(f"/vitals/weight/1/").view_name == "vitals:detail"


def test_index():
    assert (
        reverse("vitals:index")
        == f"/vitals/"
    )
    assert resolve(f"/vitals/").view_name == "vitals:index"
