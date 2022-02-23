import factory
from factory.django import DjangoModelFactory

class ClientFileFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.ClientFile'

    name = 'General_conditions.pdf'
    file = 'upload_files/General_conditions.pdf'
    language = 'ca'


class ClientFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Client'
        django_get_or_create = ('dni', 'membership_number')

    name = 'Montserrat Escayola'
    membership_number = '44630'
    dni = '34956742P'


class NotificationAddressFactory(DjangoModelFactory):
    class Meta:
        model = 'somsolet.NotificationAddress'

    client = factory.RelatedFactory(ClientFactory)
    phone_number = '631111380'
    email = 'montse@somenergia.coop'
    language = 'ca'
