# Generated by Django 2.2.7 on 2020-04-20 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0015_auto_20200406_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='sent_general_conditions',
            field=models.BooleanField(default=False, verbose_name='General conditions sent'),
        ),
    ]