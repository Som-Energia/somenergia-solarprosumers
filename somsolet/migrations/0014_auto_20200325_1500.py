# Generated by Django 2.2.7 on 2020-03-25 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0013_auto_20200123_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=9)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('language', models.CharField(choices=[('es', 'Spanish'), ('ca', 'Catalan'), ('gl', 'Galician'), ('eu', 'Euskara')], default='ca', max_length=5)),
            ],
        ),
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
            model_name='project',
            name='status',
            field=models.CharField(choices=[('empty status', 'Initial'), ('preregistered', 'Pre-Registered'), ('registered', 'Registered'), ('data downloaded', 'CCH data downloaded for analysis'), ('technical visit', 'Technical visit scheduled'), ('prereport review', 'Pre-Report review'), ('prereport', 'Pre-Report uploaded'), ('report review', 'Report review'), ('report', 'Report uploaded'), ('offer', 'Engeneering offer'), ('offer review', 'offer Review'), ('signature', 'Contract signature'), ('construction permit', 'Construction permit'), ('pending installation date', 'Pending installation date'), ('date installation set', 'Date installation set'), ('installation in progress', 'Installation in progress'), ('end installation', 'End installation'), ('legal registration', 'Legal Registration'), ('legalization', 'Legalization'), ('final payment', 'Final payment'), ('warranty payment', 'Warranty payment'), ('discarded', 'Discarded')], default='empty status', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='warning',
            field=models.CharField(choices=[('No Warn', '---'), ('Not Payed', 'Warning: Not payed'), ('prereport', 'Warning: Waiting for prereport'), ('technical visit', 'Warning: Waiting for technical visit'), ('report', 'Warning: Waiting for report'), ('offer', 'Warning: Waiting for offer'), ('signature', 'Warning: Waiting for signature'), ('installation date', 'Warning: Waiting for installation date'), ('finish installation', 'Warning: Installation deadline has passed'), ('legal registration', 'Warning: Pending registration reciept'), ('legalization', 'Warning: Waiting for legalization certificates'), ('final payment', 'Warning: Pending engeneering payment'), ('warranty payment', 'Warning: Pending warranty payment')], default='No Warn', max_length=100),
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
        migrations.AddField(
            model_name='campaign',
            name='local_group',
            field=models.ManyToManyField(related_name='campaigns', to='somsolet.LocalGroup', verbose_name='LocalGroup'),
        ),
    ]