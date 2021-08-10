from .campaign import CampaignViewSet
from .project import (CchDownloadViewSet, ProjectViewSet,
                      ReportViewSet, TechnicalDetailsViewSet,
                      FirstInvoiceViewSet, LastInvoiceViewSet)
from .stages import (StagesListViewSet, SignatureViewSet, PermitViewSet,
                     LegalRegistrationViewSet, LegalizationViewSet,
                     PrereportViewSet)
from .event import RenkontoEventView
from .stats import StatsViewSet
