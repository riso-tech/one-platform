"""
User Test Swaggers
"""
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_swagger_accessible_by_admin(admin_client):
    """test_swagger_accessible_by_admin"""
    url = reverse("api-docs")
    response = admin_client.get(url)
    assert response.status_code == 200


def test_swagger_ui_not_accessible_by_normal_user(client):
    """test_swagger_ui_not_accessible_by_normal_user"""
    url = reverse("api-docs")
    response = client.get(url, request=[])
    assert response.status_code == 403


def test_api_schema_generated_successfully(admin_client):
    """test_api_schema_generated_successfully"""
    url = reverse("api-schema")
    response = admin_client.get(url)
    assert response.status_code == 200
