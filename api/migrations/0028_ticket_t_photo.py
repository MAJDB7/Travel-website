# Generated by Django 5.0.1 on 2024-08-13 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_remove_travelplace_average_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='t_photo',
            field=models.ImageField(blank=True, null=True, upload_to='ticket_ph'),
        ),
    ]
