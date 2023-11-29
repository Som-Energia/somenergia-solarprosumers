from django.core.management.base import BaseCommand

from somrenkonto.models import Project


class Command(BaseCommand):
    help = "Migrate old fashion stages in projects to new model structure"

    PRE_REPORT_MSG = "Migrating pre-report"
    REPORT_MSG = "Migrating report"
    OFFER_MSG = "Migrating offer"
    ACCEPTED_OFFER_MSG = "Migrating accepted offer"
    SIGNATURE_MSG = "Migrating signature"
    PERMIT_MSG = "Migrating permit"
    DELIVERY_CERT_MSG = "Migrating delivery certificate"
    SECOND_INVOICE_MSG = "Migrating second invoice"
    LEGAL_REG_MSG = "Migrating legal registration"
    LEGALIZATION_MSG = "Migrating legalization"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Getting projects..."))
        projects = Project.objects.all()

        for project in projects:
            self.stdout.write(self.style.NOTICE(f"Migrating data from {project.name}"))

            self.stdout.write(self.style.NOTICE(self.PRE_REPORT_MSG))
            try:
                project.create_prereport_stage(
                    date=project.date_prereport,
                    check=project.is_invalid_prereport,
                    prereport_file=project.upload_prereport,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.REPORT_MSG))
            try:
                project.create_report_stage(
                    date=project.date_report,
                    check=project.is_invalid_report,
                    report_file=project.upload_report,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.SECOND_INVOICE_MSG))
            try:
                project.create_second_invoice_stage(
                    date=project.date_last_invoice,
                    check=project.is_paid_last_invoice,
                    second_invoice_file=project.upload_last_invoice,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.OFFER_MSG))
            try:
                project.create_offer_stage(
                    date=project.date_offer, offer_file=project.upload_offer
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.ACCEPTED_OFFER_MSG))
            try:
                project.create_accepted_offer_stage(
                    date=project.date_offer, check=project.is_invalid_offer
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.SIGNATURE_MSG))
            try:
                project.create_signature_stage(
                    date=project.date_signature,
                    check=project.is_signed,
                    signature_file=project.upload_contract,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.PERMIT_MSG))
            try:
                project.create_permit_stage(
                    date=project.date_permit,
                    check=True,
                    permit_file=project.upload_permit,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.DELIVERY_CERT_MSG))
            try:
                project.create_delivery_certificate_stage(
                    date=project.date_delivery_certificate,
                    delivery_cert_file=project.upload_delivery_certificate,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.LEGAL_REG_MSG))
            try:
                project.create_legal_registration_stage(
                    date=project.date_legal_registration_docs,
                    legal_file=project.upload_legal_registration_docs,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.NOTICE(self.LEGALIZATION_MSG))
            try:
                project.create_legalization_stage(
                    date=project.date_legal_docs,
                    rac_file=project.upload_legal_docs,
                    ritsic_file=project.upload_legal_docs,
                    cie_file=project.upload_legal_docs,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(str(e)))
