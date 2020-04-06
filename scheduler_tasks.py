import logging
from datetime import date, datetime, timedelta

from config.settings.base import BCC
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMessage
from django.db.models import Min, Q
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from somsolet.models import Campaign, Engineering, LocalGroup, Project

logger = logging.getLogger('scheduler_tasks')


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
        ).values('name', 'email')

        engineering_name = [engineering['name'] for engineering in engineering_data]
        engineering_email = [engineering['email'] for engineering in engineering_data]

        if engineering_warnings:
            logger.info("engineering_warnings")
            message_params = {
                'result': list(engineering_warnings),
                'header': _("Hola {},").format(", ".join(engineering_name)),
                'intro': _("SOM SOLET us fa arribar els WARNINGS!\
                            d’aquesta setmana:"),
                'warning_type': 'Instalació',
                'main': _("Us demanem que atengueu als diferents avisos\
                          el més aviat possible. Si us trobeu davant d’alguna\
                          incidència que us ho impedeixi, poseu-vos, siusplau,\
                          en contacte amb nosaltres per intentar solucionar\
                          l'inconvenient dels casos concrets."),
                'ending': _("Salut i fins aviat,"),
            }
            send_email(
                engineering_email,
                campaign.name,
                message_params,
                'emails/message_subject.txt',
                'emails/message_body.html',
            )
        if som_warning_final_payment:
            message_params = {
                'result': list(som_warning_final_payment),
                'header': _('Hola {},').format(", ".join(engineering_name)),
                'intro': _("Us recordem que caldria omplir la informació\
                          al document de 'fitxa tècnica' referent a cada\
                          una de les instal·lacions."),
                'warning_type': 'Project',
                'ending': _("Gràcies i fins aviat,"),
            }
            send_email(
                engineering_email,
                campaign.name,
                message_params,
                'emails/message_subject.txt',
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
                'intro': _("Per tal de poder fer-vos el retorn de la garantia\
                            disposada a l'inici de la campanya us demanem que\
                            ens feu arribar un rebut a l'adreça\
                            compres@somenergia.coop indicant el número de\
                            compte on fer la transferència."),
                'warning_type': 'Campaign',
                'ending': _('Gràcies i fins aviat,'),
            }
            send_email(
                engineering_email,
                campaign.name,
                message_params,
                'emails/message_subject.txt',
                'emails/message_body.html',
            )
        logger.info("Emails sent to engineerings.")


def send_email_summary(toSomEnergia):
    active_campaigns = Campaign.objects.filter(active=True)
    logger.info("send_email_summary")

    for campaign in active_campaigns:
        if not toSomEnergia:
            local_group_info = LocalGroup.objects.filter(
                campaigns__name=campaign.name
                ).values('email')
            email = [lg['email'] for lg in local_group_info]
        else:
            email = BCC

        projects = Project.objects.filter(
            campaign=campaign).exclude(status='discarded')
        message_params = {
            'result': {
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
            'intro': _("El SomSolet de Som Energia us envia un breu \
                    informe de l’estat de la \
                    compra col·lectiva {}".format(campaign)),
            'main': _('Per qualsevol dubte o aportació podeu fer \
                    un correu electrònic a auto@somenergia.coop'),
            'ending': _('Salut i bona energia!'),
        }
        if toSomEnergia:
            message_params['result'].update({_('Deposit'):[{'name':'To do', 'value':0}]})

        send_email(
            set(email),
            campaign.name,
            message_params,
            'emails/message_summary_subject.txt',
            'emails/message_summary_body.html',
        )


def send_email(to_email, subject, message_params, email_subject, email_template):
    to_email = to_email
    logger.info(to_email)
    subject = render_to_string(
        email_subject,
        {'campaign': subject}
    )
    html_body = render_to_string(
        email_template,
        message_params
    )
    msg = EmailMessage(
        subject,
        html_body,
        '',
        to_email,
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
        date_cch_download__lte=datetime.now() - timedelta(days=10)
    )

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
