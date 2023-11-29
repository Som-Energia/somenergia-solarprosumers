from .admin import (
    EngineeringFactory,
    InventsPacoEngineeringFactory,
    InventsPacoFactory,
    LocalGroupFactory,
    SolarWindPowerEngineeringFactory,
    SolarWindPowerFactory,
    SuperuserFactory,
    UserFactory,
)
from .campaign import CampaignFactory, TechnicalCampaignFactory
from .client import ClientFactory, ClientFileFactory
from .misc import MailingFactory
from .project import (
    ProjectDeliveryCertificateStageFactory,
    ProjectFirstFactory,
    ProjectEmptyStatusStageFactory,
    ProjectFactory,
    ProjectLegalizationStageFactory,
    ProjectLegalRegistrationStageFactory,
    ProjectOfferStageFactory,
    ProjectOfferAcceptedStageFactory,
    ProjectPermitStageFactory,
    ProjectPrereportRegisteredStageFactory,
    ProjectPrereportStageFactory,
    ProjectSecondInvoiceStageFactory,
    ProjectSignatureStageFactory,
    ProjectStageFactory,
    TechnicalDetailsFactory,
)
from .stages import (
    LegalRegistrationStageBaseFactory,
    LegalRegistrationStageFactory,
    SignatureStageBaseFactory,
    SignatureStageFactory,
)
