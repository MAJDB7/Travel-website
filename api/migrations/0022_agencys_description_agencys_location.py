# Generated by Django 5.0.1 on 2024-07-12 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_rename_airline_agencys_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencys',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='agencys',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
    ]