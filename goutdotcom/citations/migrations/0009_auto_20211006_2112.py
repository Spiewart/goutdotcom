# Generated by Django 3.1.7 on 2021-10-06 21:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0008_auto_20211006_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='accessed',
            field=models.DateField(default=datetime.datetime(2021, 10, 6, 21, 12, 47, 406635, tzinfo=utc)),
        ),
    ]