# Generated by Django 2.2.7 on 2020-04-06 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("somsolet", "0014_auto_20200325_1500"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="language",
            field=models.CharField(
                choices=[
                    ("es", "Spanish"),
                    ("ca", "Catalan"),
                    ("gl", "Galician"),
                    ("eu", "Euskara"),
                ],
                default="ca",
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name="engineering",
            name="language",
            field=models.CharField(
                choices=[
                    ("es", "Spanish"),
                    ("ca", "Catalan"),
                    ("gl", "Galician"),
                    ("eu", "Euskara"),
                ],
                default="ca",
                max_length=5,
            ),
        ),
    ]
