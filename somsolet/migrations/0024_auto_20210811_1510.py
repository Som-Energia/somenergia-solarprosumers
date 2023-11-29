# Generated by Django 2.2.24 on 2021-08-11 13:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("somsolet", "0023_campaign_count_foreseen_installations"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="notify",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="count_foreseen_installations",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Number of planned installations"
            ),
        ),
    ]
