# Generated by Django 2.2.6 on 2019-10-29 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("somsolet", "0009_auto_20191029_0910"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="campaign",
            name="engineering",
        ),
    ]
