from django.core.management.base import BaseCommand

from somsolet.models import Project


class Command(BaseCommand):
    help = 'Migrate client notification data to notification address model'

    NOTIADDRESS_MSG = 'Migrating notificaion address'
    CLIENT_FILE_MSG = 'Migrating client file'
    SENT_GENERAL_CONDITIONS_MSG = 'Migrating sent general conditions'


    def handle(self, *args, **options):

        self.stdout.write(self.style.NOTICE('Getting projects...'))
        projects = Project.objects.all()

        for project in projects:
            self.stdout.write(self.style.NOTICE(f'Migrating data from {project.client.name}'))

            self.stdout.write(self.style.NOTICE(self.NOTIADDRESS_MSG))
            try:
                project.create_notification_address(
                    client=project.client,
                    email=project.client.email,
                    phone_number=project.client.phone_number,
                    language=project.client.language
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.CLIENT_FILE_MSG))
            try:
                project.create_client_file(
                    client_file=project.client.file.first(),
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.SENT_GENERAL_CONDITIONS_MSG))
            try:
                project.create_sent_general_conditions(
                    sent_general_conditions=project.client.sent_general_conditions,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

