# Generated by Django 2.2.24 on 2021-08-12 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0028_auto_20210614_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalizationStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date File')),
                ('check', models.BooleanField(default=False, verbose_name='Checked?')),
                ('rac_file', models.FileField(default='uploaded_files/legal_docs/rac_file.png', upload_to='uploaded_files/legal_docs', verbose_name='Uploaded RAC File')),
                ('ritsic_file', models.FileField(default='uploaded_files/legal_docs/ritsic_file.png', upload_to='uploaded_files/legal_docs', verbose_name='Uploaded RITSIC File')),
                ('cie_file', models.FileField(default='uploaded_files/legal_docs/cie_file.png', upload_to='uploaded_files/legal_docs', verbose_name='Uploaded CIE File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LegalRegistrationStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date File')),
                ('check', models.BooleanField(default=False, verbose_name='Checked?')),
                ('upload', models.FileField(default='uploaded_files/legal_registration_docs/som.png', upload_to='uploaded_files/legal_registration_docs', verbose_name='Upload File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OfferStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date File')),
                ('check', models.BooleanField(default=False, verbose_name='Checked?')),
                ('upload', models.FileField(default='uploaded_files/offer/som.png', upload_to='uploaded_files/offer', verbose_name='Upload File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrereportStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date File')),
                ('check', models.BooleanField(default=False, verbose_name='Checked?')),
                ('upload', models.FileField(default='uploaded_files/prereport/som.png', upload_to='uploaded_files/prereport', verbose_name='Upload File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='PermitFile',
            new_name='PermitStage',
        ),
        migrations.RenameModel(
            old_name='SignatureFile',
            new_name='SignatureStage',
        ),
        migrations.AlterField(
            model_name='mailing',
            name='notification_status',
            field=models.CharField(choices=[('empty status', 'Initial'), ('preregistered', 'Pre-Registered'), ('registered', 'Registered'), ('data downloaded', 'CCH data downloaded for analysis'), ('technical visit', 'Technical visit scheduled'), ('prereport review', 'Pre-Report review'), ('prereport', 'Pre-Report uploaded'), ('report review', 'Report review'), ('report', 'Report uploaded'), ('offer', 'Engineering offer'), ('offer_review', 'offer Review'), ('signature', 'Contract signature'), ('first payment', 'First Payment'), ('pending payment', 'Pending Payment'), ('permit', 'Construction permit'), ('pending installation date', 'Pending installation date'), ('date installation set', 'Date installation set'), ('installation in progress', 'Installation in progress'), ('end installation', 'End installation'), ('legal registration', 'Legal Registration'), ('last payment', 'Last Payment'), ('legalization', 'Legalization'), ('final payment', 'Final payment'), ('warranty payment', 'Warranty payment'), ('discarded', 'Discarded')], default='empty status', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='permit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.PermitStage', verbose_name='Permit data'),
        ),
        migrations.AlterField(
            model_name='project',
            name='signature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.SignatureStage', verbose_name='Signature data'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('empty status', 'Initial'), ('preregistered', 'Pre-Registered'), ('registered', 'Registered'), ('data downloaded', 'CCH data downloaded for analysis'), ('technical visit', 'Technical visit scheduled'), ('prereport review', 'Pre-Report review'), ('prereport', 'Pre-Report uploaded'), ('report review', 'Report review'), ('report', 'Report uploaded'), ('offer', 'Engineering offer'), ('offer_review', 'offer Review'), ('signature', 'Contract signature'), ('first payment', 'First Payment'), ('pending payment', 'Pending Payment'), ('permit', 'Construction permit'), ('pending installation date', 'Pending installation date'), ('date installation set', 'Date installation set'), ('installation in progress', 'Installation in progress'), ('end installation', 'End installation'), ('legal registration', 'Legal Registration'), ('last payment', 'Last Payment'), ('legalization', 'Legalization'), ('final payment', 'Final payment'), ('warranty payment', 'Warranty payment'), ('discarded', 'Discarded')], default='empty status', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='legal_registration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.LegalRegistrationStage', verbose_name='Legal registration certificate'),
        ),
        migrations.AlterField(
            model_name='project',
            name='legalization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.LegalizationStage', verbose_name='Legal certificate completed'),
        ),
        migrations.AddField(
            model_name='project',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.OfferStage', verbose_name='Offer data'),
        ),
        migrations.AlterField(
            model_name='project',
            name='prereport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.PrereportStage', verbose_name='Prereport data'),
        ),
    ]