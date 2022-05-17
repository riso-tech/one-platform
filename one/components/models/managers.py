from django.conf import settings
from django.db.models import Manager
from django.utils.translation import activate, get_language


class LingualManager(Manager):
    def get_queryset_by_language(self, language, order_by=None):
        query_set = super().get_queryset().filter(language=language)
        return query_set if not order_by else query_set.order_by(order_by)

    def group_by_language(self, order_by=None):
        response = []
        activate(get_language())
        for language in settings.LANGUAGES:
            response.append(
                {
                    "language": language[0],
                    "label": language[1],
                    "data": self.get_queryset_by_language(
                        language=language[0], order_by=order_by
                    ),
                }
            )
        return response
