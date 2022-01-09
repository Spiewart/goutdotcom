# Generated by Django 3.1.7 on 2022-01-08 23:46

import datetime
from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ULTPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('dose_adjustment', models.IntegerField(default=100, help_text='What is the dose adjustment for each titration for the chosen medication?', verbose_name='Dose Adjustment')),
                ('goal_urate', models.FloatField(default=6.0, help_text='What is the goal uric acid?', verbose_name='Goal Uric Acid')),
                ('lab_interval', models.DurationField(default=datetime.timedelta(days=42), help_text='How frequently are labs required to be checked?', verbose_name='Lab Check Interval')),
                ('titrating', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='Is this ULTPlan still in the titration phase?')),
                ('last_titration', models.DateField(blank=True, help_text='When was the ULT dose last titrated?', null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
