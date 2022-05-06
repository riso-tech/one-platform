from django.contrib.auth.models import Group
from factory import Faker
from factory.django import DjangoModelFactory


class GroupFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = Group
        django_get_or_create = ["name"]
