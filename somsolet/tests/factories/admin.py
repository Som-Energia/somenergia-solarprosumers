from django.contrib.auth import get_user_model
import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username = '64959841K'


class InventsPacoFactory(UserFactory):

    username = 'N8215601I'
    email = 'info@pacoinvents.coop'
    first_name = 'Invents Paco i asociats'


class SolarWindPowerFactory(UserFactory):

    username = 'V00861641'
    email = 'info@solarwindpower.coop'
    first_name = 'Solar Wind Power'


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


class InventsPacoEngineeringFactory(EngineeringFactory):
    '''
    This engineering will have asociated events, installations and campaigns
    '''

    user = factory.SubFactory(InventsPacoFactory)
    name = factory.SelfAttribute('user.first_name')
    tin = factory.SelfAttribute('user.username')
    address = 'Carrer del Vapor Nº 24, baixos'
    email = factory.SelfAttribute('user.email')
    phone_number = '961877377'
    count_closed_projects = 1
    total_kwp_installed = 12450
    comments = 'Ingenieria de referencia en el àmbit de la autoproducció '\
               'solar fotovoltaica'


class SolarWindPowerEngineeringFactory(EngineeringFactory):
    '''
    Sample engineering without any related objects
    '''

    user = factory.SubFactory(SolarWindPowerFactory)
    name = factory.SelfAttribute('user.first_name')
    tin = factory.SelfAttribute('user.username')
    address = 'Avinguda dels Rajos Solars Nº 15'
    email = factory.SelfAttribute('user.email')
    phone_number = '956611724'
    count_closed_projects = 0
    total_kwp_installed = 0
    comments = 'Ingenieria de confiança més fresh! en àmbit del poder del '\
               'sun i el wind'
