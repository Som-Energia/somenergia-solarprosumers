# Generated by Django 2.2.16 on 2020-11-17 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0012_auto_20191025_1852'),
        ('somrenkonto', '0004_auto_20201110_1021'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='renkontoevent',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='renkontoevent',
            name='created_by',
            field=models.ForeignKey(help_text='who created this object', on_delete=django.db.models.deletion.CASCADE, related_name='renkontoevent_created', to=settings.AUTH_USER_MODEL, verbose_name='created_by'),
        ),
        migrations.AlterField(
            model_name='renkontoevent',
            name='deleted_at',
            field=models.DateTimeField(blank=True, help_text='when was deleted this object', null=True, verbose_name='deleted at'),
        ),
        migrations.AlterField(
            model_name='renkontoevent',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, help_text='last time this object updated', verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='renkontoevent',
            name='modified_by',
            field=models.ForeignKey(help_text='who modified this object', on_delete=django.db.models.deletion.CASCADE, related_name='renkontoevent_modified', to=settings.AUTH_USER_MODEL, verbose_name='modified_by'),
        ),
        migrations.CreateModel(
            name='CalendarConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='when was created this object', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='last time this object updated', verbose_name='modified at')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='when was deleted this object', null=True, verbose_name='deleted at')),
                ('calendar_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Calendar')),
                ('created_by', models.ForeignKey(help_text='who created this object', on_delete=django.db.models.deletion.CASCADE, related_name='calendarconfig_created', to=settings.AUTH_USER_MODEL, verbose_name='created_by')),
                ('modified_by', models.ForeignKey(help_text='who modified this object', on_delete=django.db.models.deletion.CASCADE, related_name='calendarconfig_modified', to=settings.AUTH_USER_MODEL, verbose_name='modified_by')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]