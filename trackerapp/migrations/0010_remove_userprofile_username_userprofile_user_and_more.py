# Generated by Django 5.1.3 on 2025-01-02 20:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackerapp', '0009_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]
