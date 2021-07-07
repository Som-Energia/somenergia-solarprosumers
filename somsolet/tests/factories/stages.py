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


class LegalRegistrationFileBaseFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.LegalRegistrationFile'

    date = '2021-06-01'
    upload =  None


class LegalRegistrationFileFactory(LegalRegistrationFileBaseFactory):

    upload = 'uploaded_files/contract/ups.png'


class LegalizationFileFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.LegalizationFile'

    date = '2021-06-01'
    rac_file =  None
    ritsic_file =  None
    cie_file =  None
