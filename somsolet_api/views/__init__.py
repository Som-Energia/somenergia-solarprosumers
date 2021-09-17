from .campaign import CampaignViewSet
from .project import (CchDownloadViewSet, ProjectViewSet,
                      ReportViewSet, TechnicalDetailsViewSet,
                      FirstInvoiceViewSet, LastInvoiceViewSet)

from .stages import (StagesListViewSet, SignatureViewSet, PermitViewSet,
                     LegalRegistrationViewSet, LegalizationViewSet,
                     PrereportViewSet, OfferViewSet, SecondInvoiceViewSet,
                     DeliveryCertificateViewSet)

from .event import RenkontoEventView
from .stats import StatsViewSet
