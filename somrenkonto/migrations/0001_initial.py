# Generated by Django 2.2.14 on 2020-07-06 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schedule', '0012_auto_20191025_1852'),
        ('somsolet', '0024_auto_20200706_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='RenkontoEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='schedule.Event')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somsolet.Campaign')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somsolet.Project')),
            ],
            bases=('schedule.event',),
        ),
    ]
