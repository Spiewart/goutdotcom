# Generated by Django 3.1.7 on 2022-01-02 14:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0010_auto_20220101_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='labcheck',
            name='completed_data',
            field=models.DateField(blank=True, default=None, help_text='When was this lab check completed?', null=True),
        ),
        migrations.AlterField(
            model_name='labcheck',
            name='due',
            field=models.DateField(default=datetime.datetime(2022, 2, 13, 14, 27, 24, 470814, tzinfo=utc), help_text='When is this lab check due?'),
        ),
    ]
