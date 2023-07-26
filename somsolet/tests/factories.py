import string

import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyText
from somsolet.models import Campaign, Client, Engineering, Project


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
        django_get_or_create = ("name",)

    name = FuzzyChoice(["Marta", "Joana", "Pol"])


class EngineeringFactory(DjangoModelFactory):
    class Meta:
        model = Engineering

    name = FuzzyText(prefix="ENG")


class CampaignFactory(DjangoModelFactory):
    class Meta:
        model = Campaign

    name = FuzzyText()
    engineerings = factory.RelatedFactory(EngineeringFactory)


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = FuzzyText(length=6, chars=string.digits, prefix="LAS")
    campaign = factory.SubFactory(CampaignFactory)
    client = factory.SubFactory(ClientFactory)
    # status = 'data downloaded'
