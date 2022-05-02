import pytest
from django.contrib.sites.models import Site

from one.contrib.sites.settings.utils import (
    setting_images_directory_path,
    site_images_directory_path,
)

pytestmark = pytest.mark.django_db


def test_setting_images_directory_path(site: Site):
    """setting_images_directory_path"""
    assert (
        setting_images_directory_path(site.setting, "1.jpg")
        == f"setting_{site.id}/images/1.jpg"
    )


def test_site_images_directory_path(site: Site):
    """site_images_directory_path"""
    assert site_images_directory_path(site, "1.jpg") == f"site_{site.id}/images/1.jpg"
