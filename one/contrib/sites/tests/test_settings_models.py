import pytest
from django.contrib.sites.models import Site

from one.contrib.sites.settings.signals import create_or_update_site_setting

pytestmark = pytest.mark.django_db


def test_site_setting_string(site: Site):
    """test_site_setting_string"""
    assert site.setting.__str__() == site.name


def test_save_site(site: Site):
    """test_save_site"""
    create_or_update_site_setting(Site, site)
    assert site.setting.__str__() == site.name


def test_logo_url(site: Site):
    """test_logo_url"""
    assert "/static/metronic/media/" in site.setting.logo_url


def test_mobile_logo_url(site: Site):
    """test_mobile_logo_url"""
    assert "/static/metronic/media/" in site.setting.mobile_logo_url
