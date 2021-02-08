# Generated by Django 2.2.17 on 2021-02-08 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0025_auto_20210208_1628'),
        ('somrenkonto', '0008_workingday'),
    ]

    operations = [
        migrations.AddField(
            model_name='renkontoevent',
            name='engineering',
            field=models.ForeignKey(default=1, help_text='Engineering related with this event', on_delete=django.db.models.deletion.CASCADE, to='somsolet.Engineering', verbose_name='Engineering'),
            preserve_default=False,
        ),
    ]
