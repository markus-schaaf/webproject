# Generated by Django 5.1.4 on 2025-01-05 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackerapp', '0021_remove_user_food_user_remove_user_workout_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyfood',
            name='intermittent_timer',
            field=models.DateTimeField(null=True),
        ),
    ]
