# Generated by Django 2.2.24 on 2021-08-10 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0030_auto_20210707_0954'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrereportFile',
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
        migrations.AddField(
            model_name='project',
            name='prereport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.PrereportFile', verbose_name='Prereport file'),
        ),
    ]
