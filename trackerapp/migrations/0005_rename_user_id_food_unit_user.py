# Generated by Django 5.1.4 on 2024-12-22 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trackerapp', '0004_alter_daily_food_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food_unit',
            old_name='user_id',
            new_name='user',
        ),
    ]
