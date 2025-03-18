# Generated by Django 5.1.5 on 2025-03-18 01:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_waterwell_users'),
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterclock',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waterclock',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='waterclock',
            name='water_well',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.waterwell'),
        ),
    ]
