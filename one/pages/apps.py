from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = "one.pages"
    verbose_name = "Pages"

    def ready(self):
        pass
