# Generated by Django 2.2.1 on 2019-10-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0006_auto_20191008_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_invalid_offer',
            field=models.BooleanField(default=False, verbose_name='Invalid Offer?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_invalid_prereport',
            field=models.BooleanField(default=False, verbose_name='Invalid Prereport?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_invalid_report',
            field=models.BooleanField(default=False, verbose_name='Invalid Report?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('empty status', 'Initial'), ('preregistered', 'Pre-Registered'), ('registered', 'Registered'), ('data downloaded', 'CCH data downloaded for analysis'), ('technical visit', 'Technical visit scheduled'), ('prereport review', 'Pre-Report review'), ('prereport', 'Pre-Report uploaded'), ('report review', 'Report review'), ('report', 'Report uploaded'), ('offer', 'Engeneering offer'), ('offer review', 'offer Review'), ('signature', 'Contract signature'), ('construction permit', 'Construction permit'), ('pending installation date', 'Pending installation date'), ('date installation set', 'Date installation set'), ('installation in progress', 'Installation in progress'), ('end installation', 'End installation'), ('legalization', 'Legalization'), ('final payment', 'Final payment'), ('warranty payment', 'Warranty payment'), ('discarded', 'Discarded')], default='empty status', max_length=50),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='acquire_interest',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='client_comments',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='contract_number',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='engineering_comments',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='installation_model',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='installation_singlephase_model',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='installation_threephase_model',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='street',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='technical_details',
            name='tariff',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
