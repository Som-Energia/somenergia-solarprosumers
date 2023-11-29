from factory import SubFactory
from factory.django import DjangoModelFactory

from .project import ProjectStageFactory


class MailingFactory(DjangoModelFactory):
    class Meta:
        model = "somsolet.Mailing"

    project = SubFactory(ProjectStageFactory)
    notification_status = "empty status"
    sent = False
