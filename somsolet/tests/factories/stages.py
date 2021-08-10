import factory
from factory.django import DjangoModelFactory


class SignatureFileBaseFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.SignatureFile'

    date = '2021-06-01'
    check = False
    upload =  None


class SignatureFileFactory(SignatureFileBaseFactory):
    upload = 'uploaded_files/contract/ups.png'


class PermitFileFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.PermitFile'

    date = '2021-06-01'
    upload = None


class OfferFileFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.OfferFile'

    date = '2021-06-29'
    check = False
    upload = None
