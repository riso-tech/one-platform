import pytest
from django.contrib.auth.models import Group

from one.utils.data_processing import getattr_in_chain

pytestmark = pytest.mark.django_db


def test_getattr_in_chain():
    group = Group.objects.create(name="Test_Chain")

    value = getattr_in_chain(group, "name")
    assert value == "Test_Chain"

    value = getattr_in_chain(group, "nam")
    assert value is None
