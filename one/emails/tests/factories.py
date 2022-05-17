from factory.django import DjangoModelFactory

from one.emails.models import AllauthTemplate


class AllauthTemplateFactory(DjangoModelFactory):
    class Meta:
        model = AllauthTemplate
