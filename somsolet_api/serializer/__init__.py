from .campaign import CampaignSerializer
from .event import RenkontoEventSerializer
from .project import (DownloadCchSerializer, ProjectSerializer,
                      TechnicalDetailsSerializer,
                      LastInvoiceSerializer)
from .stats import StatsSerializer

from .stages import (SignatureStageSerializer, PermitStageSerializer,
                     LegalRegistrationStageSerializer, LegalizationStageSerializer,
                     PrereportStageSerializer, ReportStageSerializer, OfferStageSerializer,
                     OfferAcceptedStageSerializer, SecondInvoiceStageSerializer,
                     FirstInvoiceStageSerializer, DeliveryCertificateStageSerializer)
