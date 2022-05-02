from django.contrib.sites.models import Site
from factory import Faker
from factory.django import DjangoModelFactory


class SiteFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = Site
        django_get_or_create = ["name"]
