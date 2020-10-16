# Generated by Django 2.2.16 on 2020-10-16 12:10

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('somrenkonto', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='renkontoevent',
            managers=[
                ('events', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='renkontoevent',
            name='event_type',
            field=models.CharField(default='APPO', max_length=64),
            preserve_default=False,
        ),
    ]
