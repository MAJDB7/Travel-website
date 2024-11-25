# Generated by Django 5.0.1 on 2024-07-12 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_agencys_description_agencys_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='destenation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(blank=True, choices=[('E', 'Economy'), ('B', 'Business'), ('F', 'First Class')], default='E', max_length=1, null=True),
        ),
    ]
