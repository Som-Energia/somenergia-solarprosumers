from .campaign import CampaignSerializer
from .event import RenkontoEventSerializer
from .project import (DownloadCchSerializer,
                      ProjectSerializer, ReportSerializer,
                      TechnicalDetailsSerializer,
                      FirstInvoiceSerializer, LastInvoiceSerializer)
from .stats import StatsSerializer

from .stages import (SignatureFileSerializer, PermitFileSerializer,
                     LegalRegistrationFileSerializer, LegalizationFileSerializer,
                     PrereportFileSerializer,  OfferFileSerializer)
