# Generated by Django 3.1.7 on 2022-03-26 14:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_auto_20220326_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicallabcheck',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 7, 14, 57, 15, 946094, tzinfo=utc), help_text='When is this lab check due?'),
        ),
        migrations.AlterField(
            model_name='labcheck',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 7, 14, 57, 15, 946094, tzinfo=utc), help_text='When is this lab check due?'),
        ),
    ]
