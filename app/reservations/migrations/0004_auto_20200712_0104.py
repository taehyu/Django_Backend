# Generated by Django 2.2.14 on 2020-07-12 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_auto_20200711_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='code',
        ),
        migrations.AddField(
            model_name='payment',
            name='code',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
