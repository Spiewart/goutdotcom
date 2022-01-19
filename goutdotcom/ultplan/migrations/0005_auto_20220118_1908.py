# Generated by Django 3.1.7 on 2022-01-18 19:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultplan', '0004_historicalultplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalultplan',
            name='urgent_lab_interval',
            field=models.DurationField(default=datetime.timedelta(days=14), help_text='How frequently do you recheck urgent labs?', verbose_name='Urgent Lab Check Interval'),
        ),
        migrations.AddField(
            model_name='ultplan',
            name='urgent_lab_interval',
            field=models.DurationField(default=datetime.timedelta(days=14), help_text='How frequently do you recheck urgent labs?', verbose_name='Urgent Lab Check Interval'),
        ),
    ]
