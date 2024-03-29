# Generated by Django 2.2.5 on 2019-09-18 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("somsolet", "0002_auto_20190912_0951"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="status",
            field=models.CharField(
                choices=[
                    ("empty status", "---"),
                    ("preregistered", "Pre-Registered"),
                    ("registered", "Registered"),
                    ("data downloaded", "CCH data downloaded for analysis"),
                    ("technical visit", "Technical visit scheduled"),
                    ("prereport review", "Pre-Report review"),
                    ("prereport", "Pre-Report uploaded"),
                    ("report review", "Report review"),
                    ("report", "Report uploaded"),
                    ("offer", "Engeneering offer"),
                    ("offer review", "offer Review"),
                    ("signature", "Contract signature"),
                    ("construction permit", "Construction permit"),
                    ("pending installation date", "Pending installation date"),
                    ("date installation set", "Date installation set"),
                    ("installation in progress", "Installation in progress"),
                    ("end installation", "End installation"),
                    ("legalization", "Legalization"),
                    ("final payment", "Final payment"),
                    ("warranty payment", "Warranty payment"),
                    ("discarded", "Discarded"),
                ],
                default="empty status",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_delivery_certificate",
            field=models.FileField(
                default="uploaded_files/delivery_certificate/som.png",
                upload_to="uploaded_files/delivery_certificate",
                verbose_name="Upload delivery certificate",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_legal_docs",
            field=models.FileField(
                default="uploaded_files/legal_docs/som.png",
                upload_to="uploaded_files/legal_docs",
                verbose_name="Upload legal certificate",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_offer",
            field=models.FileField(
                default="uploaded_files/offer/som.png",
                upload_to="uploaded_files/offer",
                verbose_name="Upload Offer",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_permit",
            field=models.FileField(
                default="uploaded_files/permit/som.png",
                upload_to="uploaded_files/permit",
                verbose_name="Upload Permit",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_prereport",
            field=models.FileField(
                default="uploaded_files/prereport/som.png",
                upload_to="uploaded_files/prereport",
                verbose_name="Upload Prereport",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_report",
            field=models.FileField(
                default="uploaded_files/report/som.png",
                upload_to="uploaded_files/report",
                verbose_name="Upload Report",
            ),
        ),
    ]
