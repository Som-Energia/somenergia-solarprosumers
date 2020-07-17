from factory import RelatedFactory
from factory.django import DjangoModelFactory

from .project import ProjectFactory


class MailingFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Mailing'
    
    project = RelatedFactory(ProjectFactory)
    notification_status = 'empty status'
    sent = False