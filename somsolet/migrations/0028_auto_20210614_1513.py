# Generated by Django 2.2.12 on 2021-06-14 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0027_auto_20210601_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermitFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date File')),
                ('check', models.BooleanField(default=False, verbose_name='Checked?')),
                ('upload', models.FileField(default='uploaded_files/permit/som.png', upload_to='uploaded_files/permit', verbose_name='Upload File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='project',
            name='permit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.PermitFile', verbose_name='Permit file'),
        ),
    ]
