"""
Base Components test Utils
"""

import pytest

from one.components.utils import (
    _get_fields,
    _get_lookups,
    _get_name_fields,
    _get_o2o_fields,
)
from one.users.models import User

pytestmark = pytest.mark.django_db


def test_get_name_fields():
    """test_get_name_fields"""
    model_meta = User._meta
    fields = _get_name_fields(model_meta.get_fields(include_parents=False), ["id"])
    assert len(fields) > 0


def test_get_fields():
    """test_get_fields"""
    model_meta = User._meta
    fields = _get_fields(model_meta.get_fields(include_parents=False), ["id"])
    assert len(fields) > 0


def test_get_lookups():
    """test_get_lookups"""
    model_meta = User._meta
    fields = _get_fields(model_meta.get_fields(include_parents=False))
    lookups = _get_lookups(fields[0])
    assert len(lookups) > 0


def test_get_o2o_fields():
    """test_get_o2o_fields"""
    model_meta = User._meta
    fields = _get_o2o_fields(model_meta.get_fields(include_parents=False))
    assert len(fields) > 0
