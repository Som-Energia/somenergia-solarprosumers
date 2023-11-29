# Generated by Django 2.2.7 on 2020-05-20 14:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("somsolet", "0019_auto_20200520_1630"),
    ]

    operations = [
        migrations.AlterField(
            model_name="technical_details",
            name="acquire_interest",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="acquire interest"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="administrative_division",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="Administrative division"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="anual_consumption",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="Anual Consumption (kWh)"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="bateries_brand",
            field=models.CharField(
                choices=[
                    ("SONNEN", "SONNEN"),
                    ("BYD", "BYD"),
                    ("AMPERE", "AMPERE"),
                    ("LG", "LG"),
                    ("TESLA", "TESLA"),
                ],
                max_length=50,
                verbose_name="batery brand",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="bateries_model",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="batery model"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="bateries_price",
            field=models.FloatField(blank=True, null=True, verbose_name="Batery (€)"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="charger_brand",
            field=models.BooleanField(default=False, verbose_name="charger brand"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="charger_manager",
            field=models.BooleanField(default=False, verbose_name="charger manager"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="charger_manager_brand",
            field=models.CharField(
                blank=True, max_length=22, verbose_name="Charger manager brand"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="charger_manager_model",
            field=models.CharField(
                blank=True, max_length=22, verbose_name="Charger manager model"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="client_comments",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="client comments"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="contract_number",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Contract number"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="count_shadow_optimizer",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="count shadow optimizer"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="cups",
            field=models.CharField(max_length=22, verbose_name="CUPS"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="electric_car",
            field=models.BooleanField(default=False, verbose_name="electric car"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="electric_car_charger",
            field=models.BooleanField(
                default=False, verbose_name="electric car charger"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="electric_car_charger_brand",
            field=models.CharField(
                blank=True, max_length=22, verbose_name="Electric car charger brand"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="electric_car_charger_model",
            field=models.CharField(
                blank=True, max_length=22, verbose_name="Electric car charger model"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="engineering_comments",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="engineering comments"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="homemanager",
            field=models.BooleanField(default=False, verbose_name="homemanager"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="installation_model",
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="installation_singlephase_model",
            field=models.CharField(
                blank=True,
                max_length=500,
                verbose_name="installation singlephase model",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="installation_threephase_model",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="installation threephase model"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="inversor_brand",
            field=models.CharField(
                choices=[
                    ("empty", "---"),
                    ("SMA", "SMA"),
                    ("HUAWEI", "HUAWEI"),
                    ("FRONIUS", "FRONIUS"),
                    ("KOSTAL", "KOSTAL"),
                    ("VICTRON", "VICTRON"),
                    ("ENPHASE", "ENPHASE"),
                ],
                default="empty",
                max_length=50,
                verbose_name="Inversor brand",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="inversor_model",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="Inversor model"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="municipality",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="Municipality"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="panel_brand",
            field=models.CharField(
                choices=[
                    ("empty", "---"),
                    ("REC", "REC"),
                    ("JA SOLAR", "JA SOLAR"),
                    ("JINKO", "JINKO"),
                    ("SOLARWATT", "SOLARWATT"),
                    ("PEIMAR", "PEIMAR"),
                    ("LUBI", "LUBI"),
                    ("ATERSA", "ATERSA"),
                    ("SUNPOWER", "SUNPOWER"),
                    ("C-SUN", "C-SUN"),
                    ("NOUSOL", "NOUSOL"),
                    ("SHARP", "SHARP"),
                    ("YINGLI", "YINGLI"),
                ],
                default="empty",
                max_length=22,
                verbose_name="Panel brand",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="panel_model",
            field=models.CharField(
                blank=True, max_length=22, verbose_name="Panel model"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="panel_type",
            field=models.CharField(
                choices=[("empty", "---"), ("CRISTAL", "CRISTAL"), ("OTRO", "OTRO")],
                default="empty",
                max_length=50,
                verbose_name="Panel type",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="postal_code",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Postal code"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="power_meter",
            field=models.BooleanField(default=False, verbose_name="power meter"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="roof_orientation",
            field=models.CharField(
                choices=[
                    ("empty", "---"),
                    ("N", "North"),
                    ("NNE", "North-northeast"),
                    ("NE", "Northeast"),
                    ("ENE", "East-northeast"),
                    ("E", "East"),
                    ("ESE", "East-southeast"),
                    ("SE", "Southeast"),
                    ("SSE", "South-southeast"),
                    ("S", "South"),
                    ("SSW", "South-southwest"),
                    ("SW", "Southwest"),
                    ("WSW", "West-southwest"),
                    ("W", "West"),
                    ("WNW", "West-northwest"),
                    ("NW", "Northwest"),
                    ("NNW", "North-northwest"),
                ],
                default="empty",
                max_length=50,
                verbose_name="Roof orientation",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="shadow_optimizer",
            field=models.BooleanField(default=False, verbose_name="shadow optimizer"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="shadow_optimizer_brand",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="Shadow optimizer brand"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="shadow_optimizer_model",
            field=models.CharField(
                blank=True, max_length=22, verbose_name="Shadow optimizer model"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="solar_modules_angle",
            field=models.IntegerField(
                choices=[
                    (0, 0),
                    (15, 15),
                    (30, 30),
                    (45, 45),
                    (60, 60),
                    (75, 75),
                    (90, 90),
                    (105, 105),
                    (120, 120),
                    (135, 135),
                    (150, 150),
                    (165, 165),
                    (180, 180),
                ],
                default=0,
                verbose_name="Solar models angle",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="street",
            field=models.CharField(blank=True, max_length=200, verbose_name="Street"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="tariff",
            field=models.CharField(
                blank=True, default="", max_length=200, verbose_name="tariff"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="town",
            field=models.CharField(blank=True, max_length=50, verbose_name="Town"),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="voltage",
            field=models.CharField(blank=True, max_length=50, verbose_name="voltage"),
        ),
    ]
