"""
Base Components
"""
from django.apps import AppConfig


class ComponentsConfig(AppConfig):
    """
    AppConfig of components module
    """

    name = "one.components"
    verbose_name = "Components"

    def ready(self):
        pass
