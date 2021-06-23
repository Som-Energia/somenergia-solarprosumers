from .campaign import CampaignViewSet
from .project import (CchDownloadViewSet, PrereportViewSet, ProjectViewSet,
                      ReportViewSet, TechnicalDetailsViewSet,
                      FirstInvoiceViewSet, LastInvoiceViewSet)
from .stages import (StagesListViewSet, SignatureViewSet, PermitViewSet,
                     LegalRegistrationViewSet)
from .event import RenkontoEventView
from .stats import StatsViewSet
