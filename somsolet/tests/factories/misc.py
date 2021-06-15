from factory import SubFactory
from factory.django import DjangoModelFactory

from .project import ProjectFactory


class MailingFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Mailing'

    project = SubFactory(ProjectFactory)
    notification_status = 'empty status'
    sent = False
