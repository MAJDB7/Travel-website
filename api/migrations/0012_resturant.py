# Generated by Django 5.0.1 on 2024-06-04 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_travelplace_photos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resturant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('H_photo', models.ImageField(blank=True, null=True, upload_to='hotels_ph')),
                ('rate', models.IntegerField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
