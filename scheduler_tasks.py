import logging
from datetime import datetime, timedelta

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config.settings.base import BCC
from somsolet.models import Project, Campaign

logger = logging.getLogger('scheduler_tasks')


def send_email_tasks():
    active_campaigns = Campaign.objects.filter(active=True)
    logger.info("send_email_tasks")
    for campaign in active_campaigns:
        warnings = Project.objects.filter(
            campaign=campaign).exclude(warning='No Warn')
        if warnings:
            logger.info("if warnings send emails")
            html_body = render_to_string(
                'emails/message_body.html',
                {'result': list(warnings)}
            )
            subject = render_to_string(
                "emails/message_subject.txt",
                {
                    'campaign': campaign.name
                }
            )
            msg = EmailMessage(
                subject,
                html_body,
                '',
                [campaign.engineering.email],
                BCC
            )
            msg.content_subtype = "html"
            msg.send()


def prereport_warning():
    logger.info("Start prereport_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_prereport__isnull=True,
        is_cch_downloaded=True,
        status='data downloaded',
        date_cch_download___lte=datetime.now() - timedelta(days=10)
    )

    for installation in installations:
        installation.warning = 'prereport'
        installation.warning_date = datetime.now()
        installation.save()
        logger.info("Prereport warning saved")


def technical_visit_warning():
    logger.info("Start technical_visit_warning... hoy es otro dia!")
    installations = Project.objects.filter(
        campaign__active=True,
        date_technical_visit__isnull=True,
        is_invalid_prereport=False,
        status='prereport',
        date_prereport__lte=datetime.now() - timedelta(days=7)
    )

    for installation in installations:
        installation.warning = 'technical visit'
        installation.warning_date = datetime.now()
        installation.save()
        logger.info("Technical visit warning saved")


def report_warning():
    logger.info("Start report_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_report__isnull=True,
        status='technical visit',
        date_technical_visit__lte=datetime.now() - timedelta(days=7)
    )

    for installation in installations:
        installation.warning = 'report'
        installation.warning_date = datetime.now()
        installation.save()
        logger.info("Report warning saved")


def offer_warning():
    logger.info("Start offer_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_offer__isnull=True,
        is_invalid_report=False,
        status='report',
        date_report__lte=datetime.now() - timedelta(days=5)
    )

    for installation in installations:
        installation.warning = 'offer'
        installation.warning_date = datetime.now()
        installation.save()
        logger.info("Offer warning saved")


# To Do: send mail to member
def signature_warning():
    logger.info("Start offer_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_signature__isnull=True,
        is_offer_accepted=True,
        status='offer',
        date_offer__lte=datetime.now() - timedelta(days=10)
    )

    for installation in installations:
        installation.warning = 'signature'
        installation.warning_date = datetime.now()
        installation.save()
        logger.info("Signature warning saved")


def set_date_installation_warning():
    logger.info("Start set_date_installation_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_start_installation__isnull=True,
        is_date_set=False,
        status='pending installation date',
        date_permit__lte=datetime.now() - timedelta(days=15)
    )

    for installation in installations:
        installation.warning = 'installation date'
        installation.warning_date = datetime.now()
        installation.save()
        logger.info("Set date installation warning saved")


def finish_installation_warning():
    logger.info("Start end_installation_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_delivery_certificate__isnull=True,
        status='installation in progress',
        date_start_installation__lte=datetime.now() - timedelta(days=15)
    )

    for installation in installations:
        installation.warning = 'finish installation'
        installation.warning_date = datetime.now()
        installation.save()
        logger.info("Finish installation warning saved")


def legalization_warning():
    logger.info("Start legalization_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_legal_docs__isnull=True,
        status='installation',
        date_delivery_certificate__lte=datetime.now() - timedelta(days=60)
    )

    for installation in installations:
        installation.warning = 'legalization'
        installation.warning_date = datetime.now()
        installation.save()
        logger.info("Finish legalization warning saved")
