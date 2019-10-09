# Generated by Django 2.2.1 on 2019-10-08 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0005_project_upload_contract'),
    ]

    operations = [
        migrations.RenameField(
            model_name='technical_details',
            old_name='comments',
            new_name='client_comments',
        ),
        migrations.AddField(
            model_name='technical_details',
            name='engineering_comments',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]