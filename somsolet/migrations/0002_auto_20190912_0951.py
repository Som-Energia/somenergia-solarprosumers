# Generated by Django 2.2.5 on 2019-09-12 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("somsolet", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Technical_campaign",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bateries_brand",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("SONNEN", "SONNEN"),
                            ("BYD", "BYD"),
                            ("AMPERE", "AMPERE"),
                            ("LG", "LG"),
                            ("TESLA", "TESLA"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "bateries_model",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "bateries_power",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Batery Power (kW)"
                    ),
                ),
                (
                    "bateries_capacity",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Batery Capacity (kWh)"
                    ),
                ),
                ("bateries_price", models.FloatField(blank=True, null=True)),
                ("shadow_optimizer_brand", models.CharField(max_length=50)),
                ("shadow_optimizer_model", models.CharField(max_length=22)),
                (
                    "shadow_optimizer_price",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Shadow Optimizer (€)"
                    ),
                ),
                (
                    "peak_power_panels_wp",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Panel Peak Power (Wp)"
                    ),
                ),
                (
                    "panel_brand",
                    models.CharField(
                        choices=[
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
                        max_length=22,
                    ),
                ),
                (
                    "panel_type",
                    models.CharField(
                        choices=[("CRISTAL", "CRISTAL"), ("OTRO", "OTRO")],
                        max_length=50,
                    ),
                ),
                ("panel_model", models.CharField(max_length=22)),
                (
                    "inversor_brand",
                    models.CharField(
                        choices=[
                            ("SMA", "SMA"),
                            ("HUAWEI", "HUAWEI"),
                            ("FRONIUS", "FRONIUS"),
                            ("KOSTAL", "KOSTAL"),
                            ("VICTRON", "VICTRON"),
                            ("ENPHASE", "ENPHASE"),
                        ],
                        max_length=50,
                    ),
                ),
                ("inversor_model", models.CharField(max_length=50)),
                (
                    "nominal_inversor_power",
                    models.FloatField(
                        blank=True,
                        null=True,
                        verbose_name="Nominal Inversor Power (Wn)",
                    ),
                ),
                ("charger_manager_brand", models.CharField(blank=True, max_length=22)),
                ("charger_manager_model", models.CharField(blank=True, max_length=22)),
                (
                    "charger_manager_price",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Charger manager (€)"
                    ),
                ),
                (
                    "electric_car_charger_brand",
                    models.CharField(blank=True, max_length=22),
                ),
                (
                    "electric_car_charger_model",
                    models.CharField(blank=True, max_length=22),
                ),
                (
                    "electric_car_charger_power",
                    models.FloatField(
                        blank=True,
                        null=True,
                        verbose_name="Electric Car Charger Power (kW)",
                    ),
                ),
                (
                    "electric_car_charger_price",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Electric Car Charger (€)"
                    ),
                ),
                (
                    "price_mono_fixed",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Monofasic Fixed Price (€)"
                    ),
                ),
                (
                    "price_mono_var",
                    models.FloatField(
                        blank=True,
                        null=True,
                        verbose_name="Monofasic Variable Price (€/Wp)",
                    ),
                ),
                (
                    "price_tri_fixed",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Trifasic Fixed Price (€)"
                    ),
                ),
                (
                    "price_tri_var",
                    models.FloatField(
                        blank=True,
                        null=True,
                        verbose_name="Trifasic Variable Price (€/Wp)",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="project",
            name="is_data_sent",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="bateries_brand",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="bateries_capacity",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="bateries_model",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="bateries_power",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="engineering",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="inversor_brand",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="inversor_model",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="nominal_inversor_power",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="panel_brand",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="panel_model",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="panel_type",
        ),
        migrations.RemoveField(
            model_name="technical_details",
            name="peak_power_panels_wp",
        ),
        migrations.AddField(
            model_name="campaign",
            name="active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="engineering",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="date_cch_download",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="date_delivery_certificate",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="is_cch_downloaded",
            field=models.BooleanField(default=False, verbose_name="CCH downloaded"),
        ),
        migrations.AddField(
            model_name="project",
            name="name",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="Installation"
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="upload_delivery_certificate",
            field=models.FileField(
                default="uploaded_files/som.png",
                upload_to="uploaded_files",
                verbose_name="Upload delivery certificate",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="upload_legal_docs",
            field=models.FileField(
                default="uploaded_files/som.png",
                upload_to="uploaded_files",
                verbose_name="Upload legal certificate",
            ),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="acquire_interest",
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="administrative_division",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="anual_consumption",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Anual Consumption (kWh)",
            ),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="charger_brand",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="charger_manager",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="comments",
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="count_shadow_optimizer",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="electric_car_charger",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="installation_model",
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="installation_singlephase_model",
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="installation_threephase_model",
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="municipality",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="power_meter",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="shadow_optimizer",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="technical_details",
            name="tariff",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="total_amount_penalties",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Total Penalties (€)"
            ),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="total_penalties_days",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Total Penalties (days)"
            ),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="warranty_payed_amount",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Payed Warranty (€)"
            ),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="warranty_pending_amount",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Pending Warranty (€)"
            ),
        ),
        migrations.AlterField(
            model_name="engineering",
            name="count_closed_campaigns",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Closed Campaigns"
            ),
        ),
        migrations.AlterField(
            model_name="engineering",
            name="count_closed_projects",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Closed Installations"
            ),
        ),
        migrations.AlterField(
            model_name="engineering",
            name="count_open_campaigns",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Open Campaigns"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="campaign",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="somsolet.Campaign",
                verbose_name="Campaign",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="client",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="somsolet.Client",
                verbose_name="Client",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="is_invalid_prereport",
            field=models.BooleanField(default=False, verbose_name="Invalid Prereport"),
        ),
        migrations.AlterField(
            model_name="project",
            name="is_paid",
            field=models.BooleanField(
                default=False, verbose_name="Payed Preregistration"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="preregistration_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Preregistration Date"
            ),
        ),
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
                    ("installation", "Installation"),
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
            name="upload_offer",
            field=models.FileField(
                default="uploaded_files/som.png",
                upload_to="uploaded_files",
                verbose_name="Upload Offer",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_permit",
            field=models.FileField(
                default="uploaded_files/som.png",
                upload_to="uploaded_files",
                verbose_name="Upload Permit",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_prereport",
            field=models.FileField(
                default="uploaded_files/som.png",
                upload_to="uploaded_files",
                verbose_name="Upload Prereport",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="upload_report",
            field=models.FileField(
                default="uploaded_files/som.png",
                upload_to="uploaded_files",
                verbose_name="Upload Report",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="warning",
            field=models.CharField(
                choices=[
                    ("No Warn", "---"),
                    ("Not Payed", "Warning: Not payed"),
                    ("prereport", "Warning: Waiting for prereport"),
                    ("technical visit", "Warning: Waiting for technical visit"),
                    ("report", "Warning: Waiting for report"),
                    ("offer", "Warning: Waiting for offer"),
                    ("signature", "Warning: Waiting for signature"),
                    ("installation date", "Warning: Waiting for installation date"),
                    (
                        "finish installation",
                        "Warning: Installation deadline has passed",
                    ),
                    ("legalization", "Warning: Waiting for legalization certificates"),
                ],
                default="No Warn",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="campaign",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="somsolet.Campaign",
                verbose_name="Campaign",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="client",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="somsolet.Client",
                verbose_name="Client",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="contract_number",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="count_panels",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Solar Panels"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="installation_power",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Installation Power (kW)"
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="postal_code",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="somsolet.Project",
                verbose_name="Project",
            ),
        ),
        migrations.AlterField(
            model_name="technical_details",
            name="voltage",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.DeleteModel(
            name="UserProfileInfo",
        ),
        migrations.AddField(
            model_name="technical_campaign",
            name="campaign",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="somsolet.Campaign",
                verbose_name="Campaign",
            ),
        ),
    ]
