from django.contrib.auth import get_user_model
import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username = 'N8215601I'
    email = 'info@pacoinvents.coop'
    first_name = 'Invents Paco i asociats'


class LocalGroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'somsolet.LocalGroup'

    name = 'Islas Barbados Local Group'
    phone_number = '631111380'
    email = 'islasbarbados@somenergia.coop'
    language = 'ca'


class EngineeringFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'somsolet.Engineering'
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    name = 'Invents Paco i asociats'
    tin = 'N8215601I'
    address = 'Carrer del Vapor Nº 24, baixos'
    email = 'info@pacoinvents.coop'
    phone_number = '961877377'
    count_closed_projects = 1
    total_kwp_installed = 12450
    comments = 'Ingenieria de referencia en el àmbit de la autoproducció '\
               'solar fotovoltaica'
