from .admin import (EngineeringFactory, InventsPacoFactory,
                    InventsPacoEngineeringFactory, LocalGroupFactory,
                    SolarWindPowerEngineeringFactory, SolarWindPowerFactory,
                    UserFactory, SuperuserFactory)
from .campaign import CampaignFactory, TechnicalCampaignFactory
from .client import ClientFactory, ClientFileFactory
from .misc import MailingFactory
from .project import ProjectFactory, ProjectStageFactory, TechnicalDetailsFactory
from .stages import (SignatureStageBaseFactory, SignatureStageFactory,
                     LegalRegistrationStageBaseFactory, LegalRegistrationStageFactory)
