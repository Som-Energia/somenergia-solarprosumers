import logging
import os
from datetime import date, datetime, timedelta

from config.settings import base
from config.settings.base import BCC
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMessage
from django.db.models import Min, Q
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.utils.translation import override
from somsolet.models import (Campaign, Client, ClientFile, Engineering,
                             LocalGroup, Mailing, Project)

logger = logging.getLogger('scheduler_tasks')

NOTIFICATION_TEMPLATE = {
    'prereport': 'emails/prereport.html',
}

def send_email_tasks():
    active_campaigns = Campaign.objects.filter(active=True)
    logger.info("send_email_tasks")
    for campaign in active_campaigns:
        warnings = Project.objects.filter(
            campaign=campaign).exclude(warning='No Warn')

        engineering_warnings = warnings.exclude(
            Q(warning='warranty payment') | Q(warning='final payment') | Q(status='discarded')
        )
        som_warning_final_payment = warnings.filter(
            warning='final payment'
        )
        som_warning_warranty = warnings.filter(
            warning='warranty payment'
        ).distinct('campaign')

        engineering_data = Engineering.objects.filter(
            campaigns__name=campaign.name
        ).values('name', 'email', 'language')

        engineering_name = [engineering['name'] for engineering in engineering_data]
        engineering_email = [engineering['email'] for engineering in engineering_data]
        engineering_language = [engineering['language'] for engineering in engineering_data][0]

        if engineering_warnings:
            with override(engineering_language):
                logger.info("engineering_warnings")
                message_params = {
                    'result': list(engineering_warnings),
                    'header': _("Hola {},").format(", ".join(engineering_name)),
                    'intro': _("SOM SOLET us fa arribar els WARNINGS! d’aquesta setmana:"),
                    'warning_type': _('Instalació'),
                    'main': _("Us demanem que atengueu als diferents avisos el més aviat possible. Si us trobeu davant d’alguna incidència que us ho impedeixi, poseu-vos, siusplau, en contacte amb nosaltres per intentar solucionar l'inconvenient dels casos concrets."),
                    'ending': _("Salut i fins aviat,"),
                }
                send_email(
                    engineering_email,
                    render_to_string(
                            'emails/message_subject.txt',
                            {'campaign': campaign.name}
                    ),
                    message_params,
                    'emails/message_body.html',
                )
        if som_warning_final_payment:
            message_params = {
                'result': list(som_warning_final_payment),
                'header': _('Hola {},').format(", ".join(engineering_name)),
                'intro': _("Us recordem que caldria omplir la informació al document de 'fitxa tècnica' referent a cada una de les instal·lacions."),
                'warning_type': _('Project'),
                'ending': _("Gràcies i fins aviat,"),
            }
            send_email(
                engineering_email,
                render_to_string(
                    'emails/message_subject.txt',
                    {'campaign': campaign.name}
                ),
                message_params,
                'emails/message_body.html',
            )
        if som_warning_warranty:
            campaign_warning = []
            for project in som_warning_warranty:
                campaign_warning.append({
                    'name': project.campaign.name,
                    'warning': project.warning
                })
            message_params = {
                'result': campaign_warning,
                'header': _("Hola {},").format(", ".join(engineering_name)),
                'intro': _("Per tal de poder fer-vos el retorn de la garantia disposada a l'inici de la campanya us demanem que ens feu arribar un rebut a l'adreça compres@somenergia.coop indicant el número de compte on fer la transferència."),
                'warning_type': _('Campaign'),
                'ending': _('Gràcies i fins aviat,'),
            }
            send_email(
                engineering_email,
                render_to_string(
                    'emails/message_subject.txt',
                    {'campaign': campaign.name}
                ),
                campaign.name,
                message_params,
                'emails/message_body.html',
            )
        logger.info("Emails sent to engineerings.")


def send_notification():
    notifications_to_send = Mailing.objects.filter(
        sent=False
    )
    logger.info('sending notifications')
    for noti in notifications_to_send:
        campaign_data = Campaign.objects.filter(name=noti.project.campaign).values(
            'count_foreseen_installations',
            'engineerings__name',
            'engineerings__address',
            'engineerings__email'
        )

        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i bona energia,"),
            'campaign': noti.project.campaign,
            'address': [data['engineerings__address'] for data in campaign_data][0],
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'installations': [data['count_foreseen_installations'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0]
        }

        send_notification_report(
            noti,
            _(f'PREINFORME - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            NOTIFICATION_TEMPLATE[noti.notification_status],
            message_params,
            str(os.path.join(base.MEDIA_ROOT, str(noti.project.prereport.file_upload))),
            message_params['email'],
        )

def send_prereport_notification():
    notifications_to_send = Mailing.objects.filter(
        notification_status='prereport',
        sent=False
    )
    logger.info('sending prereort')
    for noti in notifications_to_send:
        campaign_data = Campaign.objects.filter(name=noti.project.campaign).values(
            'count_foreseen_installations',
            'engineerings__name',
            'engineerings__address',
            'engineerings__email'
        )

        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i bona energia,"),
            'campaign': noti.project.campaign,
            'address': [data['engineerings__address'] for data in campaign_data][0],
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'installations': [data['count_foreseen_installations'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0]
        }

        send_notification_report(
            noti,
            _(f'PREINFORME - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'emails/prereport.html',
            message_params,
            str(os.path.join(base.MEDIA_ROOT, str(noti.project.upload_prereport))),
            message_params['email'],
        )


def send_notification_report(notification, subject, template, message_params, attachment=False, from_email=''):

    with override(notification.project.client.language):
        send_email(
            [notification.project.client.email],
            subject,
            message_params,
            template,
            attachment,
            from_email,
        )
        notification.sent = True
        notification.save()


def send_email_summary(toSomEnergia, toEngineering, toGL):
    active_campaigns = Campaign.objects.filter(active=True)
    logger.info("send_email_summary")

    for campaign in active_campaigns:
        if toSomEnergia:
            email = BCC
            message_params = stats_report(toSomEnergia, campaign, 'ca')
            language = 'ca'
        if toEngineering:
            engineering_info = Engineering.objects.filter(
                campaigns__name=campaign.name
            ).values('email', 'language')
            email = [eng['email'] for eng in engineering_info]
            language = [eng['language'] for eng in engineering_info][0]
            message_params = stats_report(toSomEnergia, campaign, language)
        if toGL:
            local_group_info = LocalGroup.objects.filter(
                campaigns__name=campaign.name
            ).values('email', 'language')
            email = [lg['email'] for lg in local_group_info]
            language = [lg['language'] for lg in local_group_info][0]
            message_params = stats_report(toSomEnergia, campaign, language)
        with override(language):
            send_email(
                list(set(email)),
                render_to_string(
                    'emails/message_summary_subject.txt',
                    {'campaign': campaign.name}
                ),
                message_params,
                'emails/message_summary_body.html',
            )


def stats_report(toSomEnergia, campaign, language):
    projects = Project.objects.filter(
        campaign=campaign).exclude(status='discarded')
    logger.info('language')
    message_params = {
        'result':
            {
                _('Prereports'): prereport_summary(projects),
                _('Technical Visits'): technical_visit_summary(projects),
                _('Signed Contracts'): signature_summary(projects),
                _('Construction Permits'): construction_permits_summary(projects),
                _('Installations'): installation_summary(projects),
                _('legalization'): legalization_summary(projects),
                _('Discarded inscriptions'): discarded_summary(campaign),
            },
        'campaign_info': campaign_info(campaign),
        'header': _("Hola,"),
        'intro': _("El SomSolet de Som Energia us envia un breu informe de l’estat de la compra col·lectiva."),
        'main': _('Per qualsevol dubte o aportació podeu fer un correu electrònic a auto@somenergia.coop'),
        'ending': _('Salut i bona energia!'),
    }
    if toSomEnergia:
        message_params['result'].update(
            {
                _('Deposit'): [{'name': 'To do', 'value': 0}]
            }
        )
    return message_params


def send_email(to_email, subject, message_params, email_template, filename=False, from_email=''):
    logger.info(to_email)
    html_body = render_to_string(
        email_template,
        message_params
    )
    msg = EmailMessage(
        subject,
        html_body,
        from_email,
        to_email,
        BCC,
    )
    if filename:
        msg.attach_file(filename)
    msg.content_subtype = "html"
    msg.send()


def prereport_warning():
    logger.info("Start prereport_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_prereport__isnull=True,
        status='registered',
        registration_date__lte=datetime.now() - timedelta(days=10)
    ).exclude(warning='prereport')

    for installation in installations:
        installation.warning = 'prereport'
        installation.warning_date = datetime.now()
        installation.save()
        msg = "Finish prereport warning saved for: {}"
        logger.info(msg.format(installation.name))


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
        msg = "Finish technical visit warning saved for: {}"
        logger.info(msg.format(installation.name))


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
        msg = "Finish report warning saved for: {}"
        logger.info(msg.format(installation.name))


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
        msg = "Finish offer warning saved for: {}"
        logger.info(msg.format(installation.name))


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
        msg = "Finish signature warning saved for: {}"
        logger.info(msg.format(installation.name))


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
        msg = "Finish set date installation warning saved for: {}"
        logger.info(msg.format(installation.name))


def finish_installation_warning():
    logger.info("Start end_installation_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_delivery_certificate__isnull=True,
        status='installation in progress',
        date_start_installation__lte=datetime.now() - timedelta(days=10)
    )

    for installation in installations:
        installation.warning = 'finish installation'
        installation.warning_date = datetime.now()
        installation.save()
        msg = "Finish installation warning saved for: {}"
        logger.info(msg.format(installation.name))


def legal_registration_warning():
    logger.info("Start legal_registration_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_legal_registration_docs__isnull=True,
        status='end installation',
        date_delivery_certificate__lte=datetime.now() - timedelta(days=60)
    )

    for installation in installations:
        installation.warning = 'legal registration'
        installation.warning_date = datetime.now()
        installation.save()
        msg = "Finish legal registration warning saved for: {}"
        logger.info(msg.format(installation.name))


def legalization_warning():
    logger.info("Start legalization_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_legal_docs__isnull=True,
        status='legal registration',
        date_legal_registration_docs__lte=datetime.now() - timedelta(days=15)
    )

    for installation in installations:
        installation.warning = 'legalization'
        installation.warning_date = datetime.now()
        installation.save()
        msg = "Finish legalization warning saved for: {}"
        logger.info(msg.format(installation.name))


def final_payment_warning():
    logger.info("Start final_payment_warning...")
    installations = Project.objects.filter(
        campaign__active=True,
        date_legal_docs__isnull=False,
        status='legalization',
        date_legal_docs__lte=datetime.now() - timedelta(days=21)
    )

    for installation in installations:
        installation.warning = 'final payment'
        installation.warning_date = datetime.now()
        installation.save()
        msg = "Finish final payment warning saved for: {}"
        logger.info(msg.format(installation.name))


def warranty_warning():
    logger.info("Start warranty_warning...")
    legalized_campaigns = Campaign.objects.filter(
        active=True).exclude(
        project__date_legal_docs__isnull=True)
    for campaign in legalized_campaigns:
        warranty_deadline = Project.objects.filter(
            campaign=campaign).order_by(
            '-date_legal_docs').first().date_legal_docs + relativedelta(
            months=+24)
        installations = Project.objects.filter(
            campaign=campaign)
        if datetime.now().date() >= warranty_deadline:
            installations = Project.objects.filter(campaign=campaign)
            for installation in installations:
                installation.warning = 'warranty payment'
                installation.warning_date = datetime.now()
                installation.save()
            msg = "Finish warranty warning saved for: {}"
            logger.info(msg.format(campaign.name))
        else:
            logger.info("there are no warrings to send")


def campaign_info(campaign):
    return {
        _('Summary date'): date.today().strftime("%d/%m/%Y"),
        _('Date inscriptions start'): campaign.date_call_for_inscriptions.strftime("%d/%m/%Y"),
        _('Total inscriptions'): Project.objects.filter(
                campaign=campaign).count(),
    }


def prereport_summary(projects):
    sent_prereport = projects.filter(date_prereport__isnull=False).count()
    unsent_prereport = projects.filter(date_prereport__isnull=True).count()

    prereport_summary = [
        {'name': _('Sent Prereports'), 'value': sent_prereport},
        {'name': _('Unsent Prereports'), 'value': unsent_prereport},
    ]
    overdue_prereport = projects.filter(warning='prereport').count()
    if overdue_prereport:
        max_overdue_prereport = projects.filter(warning='prereport').aggregate(
            Min('warning_date')
        )
        prereport_summary.extend([
            {
                'name': _('Overdue Prereports'),
                'value': overdue_prereport
            },
            {
                'name': _('Maximum overdue days'),
                'value': (date.today() - max_overdue_prereport['warning_date__min']).days
            },
        ])
    return prereport_summary


def technical_visit_summary(projects):
    prereport_status = projects.filter(status='prereport')
    pending_visits = prereport_status.filter(date_technical_visit__isnull=True).count()
    scheduled_visits = projects.filter(date_technical_visit__isnull=False).exclude(
        date_report__isnull=False).count()
    visits_done = projects.filter(date_report__isnull=False).count()
    summary = [
        {
            'name': _('Technical Visits Pending'),
            'value': pending_visits
        },
        {
            'name': _('Technical Visits Calendarized'),
            'value': scheduled_visits
        },
        {
            'name': _('Technical Visits Done'),
            'value': visits_done
        },
    ]
    overdue = projects.filter(warning='technical visit')
    if overdue:
        max_overdue = overdue.aggregate(Min('warning_date'))['warning_date__min']
        summary.extend([
            {
                'name': _('Overdue Technical Visits'),
                'value': overdue.count()
            },
            {
                'name': _('Maximum Overdue Days'),
                'value': (date.today() - max_overdue).days
            },
        ])
    return summary


def signature_summary(projects):
    uploaded_offers = projects.filter(date_offer__isnull=False).filter(
        is_invalid_offer=False).count()
    signed_contracts = projects.filter(date_signature__isnull=False).count()
    overdue_contracts = projects.filter(warning='signature')
    summary = [
        {
            'name': _('Submitted Offers'),
            'value': uploaded_offers
        },
        {
            'name': _('Signed Contracts'),
            'value': signed_contracts
        },
        {
            'name': _('Signature Pending Contracts'),
            'value': uploaded_offers - signed_contracts
        }
    ]
    if overdue_contracts:
        max_overdue = overdue_contracts.aggregate(
            Min('warning_date')
        )['warning_date__min']
        summary.extend([
            {
                'name': _('Overdue Signed Contracts'),
                'value': overdue_contracts.count()
            },
            {
                'name': _('Maximum Overdue Days'),
                'value': (date.today() - max_overdue).days
            }
        ])
    return summary


def construction_permits_summary(projects):
    pending_permits = projects.filter(status='signature').count()
    accepted_permits = projects.filter(date_permit__isnull=False).count()

    return [
        {
            'name': _('Construction Permits Pending'),
            'value': pending_permits
        },
        {
            'name': _('Accepted Construction Permits'),
            'value': accepted_permits
        },
    ]


def installation_summary(projects):
    installation_summary = []

    scheduled_installations = projects.filter(
        status='date installation set'
    ).count()
    incompleted_installations = projects.filter(
        date_start_installation__isnull=False).exclude(
        date_delivery_certificate__isnull=False
    ).count()
    finished_installations = projects.filter(
        date_delivery_certificate__isnull=False
    ).count()
    installation_summary = [
        {
            'name': _('Scheduled installations'),
            'value': scheduled_installations
        },
        {
            'name': _('Incompleted installations'),
            'value': incompleted_installations
        },
        {
            'name': _('Finished installations'),
            'value': finished_installations
        }
    ]
    overdue_installations = projects.filter(
        warning='finish installation'
    ).count()

    if overdue_installations:
        installation_summary.append({
            'name': _('Overdue installations by more than five days'),
            'value': overdue_installations
        })
    return installation_summary


def legalization_summary(projects):
    pending_registration = projects.filter(
        date_delivery_certificate__isnull=False).exclude(
        date_legal_registration_docs__isnull=False
    ).count()
    pending_approval = projects.filter(
        date_legal_registration_docs__isnull=False).exclude(
        date_legal_docs__isnull=False
    ).count()
    legalized_installations = projects.filter(
        date_legal_docs__isnull=False
    ).count()
    legalization_summary = [
        {
            'name': _('Installations pending registration'),
            'value': pending_registration
        },
        {
            'name': _('Registered installations pending approval'),
            'value': pending_approval
        },
        {
            'name': _('Legalized installations'),
            'value': legalized_installations
        }
    ]

    overdue_pending_registration = projects.filter(
        warning='legal registration'
    ).count()
    if overdue_pending_registration:
        max_overdue_pending_registration = projects.filter(
            warning='legal registration').aggregate(Min('warning_date'))
        legalization_summary.extend([
            {
                'name': _('Overdue pending registration'),
                'value': overdue_pending_registration
            },
            {
                'name': _('Maximum overdue days'),
                'value': (date.today() - max_overdue_pending_registration['warning_date__min']).days
            }
        ])

    overdue_pending_approval = projects.filter(
        warning='legalization'
    ).count()
    if overdue_pending_approval:
        max_overdue_pending_approval = projects.filter(
            warning='legalization'
        ).aggregate(Min('warning_date'))
        legalization_summary.extend([
            {
                'name': _('Overdue pending registration'),
                'value': overdue_pending_approval
            },
            {
                'name': _('Maximum overdue days'),
                'value': (date.today() - max_overdue_pending_approval['warning_date__min']).days,
            }
        ])
    return legalization_summary


def discarded_summary(campaign):
    projects = Project.objects.filter(campaign=campaign)
    discarded_technical = projects.filter(discarded_type='technical').count()
    discarded_voluntary = projects.filter(discarded_type='voluntary').count()

    discarded_summary = [
        {'name': _('Technical'), 'value': discarded_technical},
        {'name': _('Voluntary'), 'value': discarded_voluntary}
    ]
    return discarded_summary
