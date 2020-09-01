import django_rq
from django.apps import AppConfig


class SomsoletConfig(AppConfig):
    name = 'somsolet'

    def ready(self):
        scheduler = django_rq.get_scheduler('default')

        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            scheduler.cancel(job)

        import scheduler_tasks

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.send_prereport_notification,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 22 * * 6",
            func=scheduler_tasks.send_email_tasks,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 22 * * 6",
            func=scheduler_tasks.send_email_summary,
            args=[True, False],
            repeat=1,
            queue_name='default',
        )
        scheduler.cron(
            "0 22 1,15 * *",
            func=scheduler_tasks.send_email_summary,
            args=[False, True],
            repeat=1,
            queue_name='default',
        )
        scheduler.cron(
            "0 22 1,15 * *",
            func=scheduler_tasks.send_email_summary,
            args=[False, False],
            repeat=1,
            queue_name='default',
        )
        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.prereport_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.technical_visit_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.report_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.offer_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.signature_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.set_date_installation_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.finish_installation_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.legal_registration_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.legalization_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 1 * *",
            func=scheduler_tasks.final_payment_warning,
            repeat=1,
            queue_name='default',
        )

        scheduler.cron(
            "0 23 * * *",
            func=scheduler_tasks.warranty_warning,
            repeat=1,
            queue_name='default',
        )
