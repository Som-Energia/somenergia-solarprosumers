import factory
from factory.django import DjangoModelFactory


class PrereportStageFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.PrereportStage'

    date = '2021-06-01'
    upload = None
    check = False


class SignatureStageBaseFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.SignatureStage'

    date = '2021-06-01'
    check = False
    upload =  None


class SignatureStageFactory(SignatureStageBaseFactory):
    upload = 'uploaded_files/contract/ups.png'


class PermitStageFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.PermitStage'

    date = '2021-06-01'
    upload = None


class OfferStageFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.OfferStage'

    date = '2021-06-29'
    check = False
    upload = None

class LegalRegistrationStageBaseFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.LegalRegistrationStage'

    date = '2021-06-01'
    upload =  None


class LegalRegistrationStageFactory(LegalRegistrationStageBaseFactory):

    upload = 'uploaded_files/contract/ups.png'


class LegalizationStageFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.LegalizationStage'

    date = '2021-06-01'
    rac_file =  None
    ritsic_file =  None
    cie_file =  None
