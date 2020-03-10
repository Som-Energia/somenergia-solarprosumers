# Generated by Django 2.2.6 on 2020-01-23 08:50

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0010_remove_campaign_engineering'),
    ]

    operations = [
        migrations.AddField(
            model_name='technical_details',
            name='bateries_brand',
            field=models.CharField(blank=True, choices=[('SONNEN', 'SONNEN'), ('BYD', 'BYD'), ('AMPERE', 'AMPERE'), ('LG', 'LG'), ('TESLA', 'TESLA')], max_length=50),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='bateries_model',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='bateries_power',
            field=models.FloatField(blank=True, null=True, verbose_name='Batery Power (kW)'),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='bateries_capacity',
            field=models.FloatField(blank=True, null=True, verbose_name='Batery Capacity (kWh)'),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='bateries_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='shadow_optimizer_brand',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='shadow_optimizer_model',
            field=models.CharField(max_length=22, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='shadow_optimizer_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Shadow Optimizer (€)'),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='peak_power_panels_wp',
            field=models.FloatField(blank=True, null=True, verbose_name='Panel Peak Power (Wp)'),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='panel_brand',
            field=models.CharField(choices=[('REC', 'REC'), ('JA SOLAR', 'JA SOLAR'), ('JINKO', 'JINKO'), ('SOLARWATT', 'SOLARWATT'), ('PEIMAR', 'PEIMAR'), ('LUBI', 'LUBI'), ('ATERSA', 'ATERSA'), ('SUNPOWER', 'SUNPOWER'), ('C-SUN', 'C-SUN'), ('NOUSOL', 'NOUSOL'), ('SHARP', 'SHARP'), ('YINGLI', 'YINGLI')], max_length=22, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='panel_type',
            field=models.CharField(choices=[('CRISTAL', 'CRISTAL'), ('OTRO', 'OTRO')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='panel_model',
            field=models.CharField(max_length=22, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='electric_car_charger_brand',
            field=models.CharField(blank=True, max_length=22),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='electric_car_charger_model',
            field=models.CharField(blank=True, max_length=22),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='electric_car_charger_power',
            field=models.FloatField(blank=True, null=True, verbose_name='Electric Car Charger Power (kW)'),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='electric_car_charger_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Electric Car Charger (€)'),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='charger_manager_brand',
            field=models.CharField(blank=True, max_length=22),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='charger_manager_model',
            field=models.CharField(blank=True, max_length=22),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='charger_manager_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Charger manager (€)'),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='inversor_brand',
            field=models.CharField(choices=[('SMA', 'SMA'), ('HUAWEI', 'HUAWEI'), ('FRONIUS', 'FRONIUS'), ('KOSTAL', 'KOSTAL'), ('VICTRON', 'VICTRON'), ('ENPHASE', 'ENPHASE')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='inversor_model',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='technical_details',
            name='nominal_inversor_power',
            field=models.FloatField(blank=True, null=True, verbose_name='Nominal Inversor Power (Wn)')
        ),
    ]