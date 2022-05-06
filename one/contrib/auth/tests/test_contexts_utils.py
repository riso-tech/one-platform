import pytest
from django.contrib.auth.models import Group

from one.contrib.auth.contexts.utils import (
    group_context_images_directory_path,
    group_images_directory_path,
)

pytestmark = pytest.mark.django_db


def test_group_images_directory_path(group: Group):
    """group_images_directory_path"""
    assert (
        group_images_directory_path(group, "1.jpg") == f"group_{group.id}/images/1.jpg"
    )


def test_group_context_images_directory_path(group: Group):
    """group_context_images_directory_path"""
    assert (
        group_context_images_directory_path(group.context, "1.jpg")
        == f"group_context_{group.id}/images/1.jpg"
    )
