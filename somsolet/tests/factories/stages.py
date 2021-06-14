import factory
from factory.django import DjangoModelFactory


class SignatureFileFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.SignatureFile'
    
    date = '2021-06-01'
    check = False
    upload = None

class PermitFileFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.PermitFile'

    date = '2021-06-01'
    upload = None