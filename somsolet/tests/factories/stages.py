import factory
from factory.django import DjangoModelFactory


class PrereportFileFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.PrereportFile'

    date = '2021-06-01'
    upload = None
    check = False


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
