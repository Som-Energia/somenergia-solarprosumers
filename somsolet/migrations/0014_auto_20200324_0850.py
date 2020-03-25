# Generated by Django 2.2.7 on 2020-03-24 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0013_auto_20200123_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='date_legal_registration_docs',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='upload_legal_registration_docs',
            field=models.FileField(default='uploaded_files/legal_registration_docs/som.png', upload_to='uploaded_files/legal_registration_docs', verbose_name='Upload legal registration certificate'),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='inversor_brand',
            field=models.CharField(choices=[('empty', '---'), ('SMA', 'SMA'), ('HUAWEI', 'HUAWEI'), ('FRONIUS', 'FRONIUS'), ('KOSTAL', 'KOSTAL'), ('VICTRON', 'VICTRON'), ('ENPHASE', 'ENPHASE')], default='empty', max_length=50),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='inversor_model',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='panel_brand',
            field=models.CharField(choices=[('empty', '---'), ('REC', 'REC'), ('JA SOLAR', 'JA SOLAR'), ('JINKO', 'JINKO'), ('SOLARWATT', 'SOLARWATT'), ('PEIMAR', 'PEIMAR'), ('LUBI', 'LUBI'), ('ATERSA', 'ATERSA'), ('SUNPOWER', 'SUNPOWER'), ('C-SUN', 'C-SUN'), ('NOUSOL', 'NOUSOL'), ('SHARP', 'SHARP'), ('YINGLI', 'YINGLI')], default='empty', max_length=22),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='panel_model',
            field=models.CharField(blank=True, max_length=22, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='panel_type',
            field=models.CharField(choices=[('empty', '---'), ('CRISTAL', 'CRISTAL'), ('OTRO', 'OTRO')], default='empty', max_length=50),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='shadow_optimizer_brand',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='shadow_optimizer_model',
            field=models.CharField(blank=True, max_length=22, null=True),
        ),
    ]