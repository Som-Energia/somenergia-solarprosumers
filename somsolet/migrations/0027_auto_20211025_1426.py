# Generated by Django 2.2.24 on 2021-10-25 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0026_delivery_certificate_20210923'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferAcceptedStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date File')),
                ('check', models.BooleanField(default=False, verbose_name='Checked?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReportStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date File')),
                ('check', models.BooleanField(default=False, verbose_name='Checked?')),
                ('upload', models.FileField(default='uploaded_files/report/som.png', upload_to='uploaded_files/report', verbose_name='Upload File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='mailing',
            name='notification_status',
            field=models.CharField(choices=[('empty status', 'Initial'), ('preregistered', 'Pre-Registered'), ('registered', 'Registered'), ('data downloaded', 'CCH data downloaded for analysis'), ('technical visit', 'Technical visit scheduled'), ('prereport review', 'Pre-Report review'), ('prereport', 'Pre-Report uploaded'), ('report review', 'Report review'), ('report', 'Report uploaded'), ('offer', 'Engineering offer'), ('offer accepted', 'Engineering offer accepted'), ('offer review', 'offer Review'), ('signature', 'Contract signature'), ('first payment', 'First Payment'), ('pending payment', 'Pending Payment'), ('permit', 'Construction permit'), ('pending installation date', 'Pending installation date'), ('date installation set', 'Date installation set'), ('installation in progress', 'Installation in progress'), ('end installation', 'End installation'), ('second invoice', 'Second Payment'), ('legal registration', 'Legal Registration'), ('last payment', 'Last Payment'), ('legalization', 'Legalization'), ('final payment', 'Final payment'), ('warranty payment', 'Warranty payment'), ('discarded', 'Discarded')], default='empty status', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('empty status', 'Initial'), ('preregistered', 'Pre-Registered'), ('registered', 'Registered'), ('data downloaded', 'CCH data downloaded for analysis'), ('technical visit', 'Technical visit scheduled'), ('prereport review', 'Pre-Report review'), ('prereport', 'Pre-Report uploaded'), ('report review', 'Report review'), ('report', 'Report uploaded'), ('offer', 'Engineering offer'), ('offer accepted', 'Engineering offer accepted'), ('offer review', 'offer Review'), ('signature', 'Contract signature'), ('first payment', 'First Payment'), ('pending payment', 'Pending Payment'), ('permit', 'Construction permit'), ('pending installation date', 'Pending installation date'), ('date installation set', 'Date installation set'), ('installation in progress', 'Installation in progress'), ('end installation', 'End installation'), ('second invoice', 'Second Payment'), ('legal registration', 'Legal Registration'), ('last payment', 'Last Payment'), ('legalization', 'Legalization'), ('final payment', 'Final payment'), ('warranty payment', 'Warranty payment'), ('discarded', 'Discarded')], default='empty status', help_text='State of the project', max_length=50, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='project',
            name='offer_accepted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.OfferAcceptedStage', verbose_name='Offer data'),
        ),
        migrations.AddField(
            model_name='project',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.ReportStage', verbose_name='Report data'),
        ),
    ]
