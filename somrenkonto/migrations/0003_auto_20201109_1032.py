# Generated by Django 2.2.16 on 2020-11-09 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('somrenkonto', '0002_auto_20201016_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='renkontoevent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='when was created this object', verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='renkontoevent',
            name='created_by',
            field=models.ForeignKey(default=1, help_text='who created this object', on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to=settings.AUTH_USER_MODEL, verbose_name='created_by'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='renkontoevent',
            name='deleted_at',
            field=models.DateTimeField(blank=True, help_text='when was deleted this object', null=True, verbose_name='created_by'),
        ),
        migrations.AddField(
            model_name='renkontoevent',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, help_text='last update of this object', verbose_name='created_by'),
        ),
        migrations.AddField(
            model_name='renkontoevent',
            name='modified_by',
            field=models.ForeignKey(default=1, help_text='who modified this object', on_delete=django.db.models.deletion.CASCADE, related_name='modified_events', to=settings.AUTH_USER_MODEL, verbose_name='created_by'),
            preserve_default=False,
        ),
    ]