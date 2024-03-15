import factory
from factory.django import DjangoModelFactory


class PrereportStageFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.PrereportStage"

    date = "2021-06-01"
    upload = None
    _check = False


class ReportBaseStageFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.ReportStage"

    date = "2021-06-01"
    upload = None
    _check = False


class ReportStageFactory(ReportBaseStageFactory):
    upload = "uploaded_files/contract/ups.png"


class SignatureStageBaseFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.SignatureStage"

    date = "2021-06-01"
    _check = False
    upload = None


class SignatureStageFactory(SignatureStageBaseFactory):
    upload = "uploaded_files/contract/ups.png"


class PermitStageFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.PermitStage"

    date = "2021-06-01"
    upload = None


class OfferBaseStageFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.OfferStage"

    date = "2021-06-29"
    upload = None


class OfferStageFactory(OfferBaseStageFactory):
    upload = "uploaded_files/contract/ups.png"


class OfferAcceptedStageFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.OfferAcceptedStage"

    date = "2021-06-29"
    _check = False


class SecondInvoiceStageFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.SecondInvoiceStage"

    date = "2021-06-29"
    _check = False
    upload = None


class LegalRegistrationStageBaseFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.LegalRegistrationStage"

    date = "2021-06-01"
    upload = None


class LegalRegistrationStageFactory(LegalRegistrationStageBaseFactory):
    upload = "uploaded_files/contract/ups.png"


class LegalizationStageFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.LegalizationStage"

    date = "2021-06-01"
    rac_file = None
    ritsic_file = None
    cie_file = None


class DeliveryCertificateStageFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.DeliveryCertificateStage"

    date = "2021-06-01"
    upload = None
