# Generated by Django 2.2.17 on 2021-02-08 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('somsolet', '0024_auto_20200706_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='engineering',
            field=models.ForeignKey(blank=True, help_text='Engineering responsable of this project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.Engineering', verbose_name='Engineering'),
        ),
        migrations.AlterField(
            model_name='project',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='somsolet.Campaign', verbose_name='Campaign'),
        ),
    ]