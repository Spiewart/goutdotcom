# Generated by Django 3.1.7 on 2022-01-21 20:52

import datetime
from django.db import migrations, models
import django_extensions.db.fields
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalULTPlan',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('dose_adjustment', models.IntegerField(default=100, help_text='What is the dose adjustment for each titration for the chosen medication?', verbose_name='Dose Adjustment')),
                ('goal_urate', models.FloatField(default=6.0, help_text='What is the goal uric acid?', verbose_name='Goal Uric Acid')),
                ('titration_lab_interval', models.DurationField(default=datetime.timedelta(days=42), help_text='How frequently are labs required to be checked duration ULT titration?', verbose_name='Titration Lab Check Interval')),
                ('monitoring_lab_interval', models.DurationField(default=datetime.timedelta(days=180), help_text='How frequently are labs required to be checked during routine monitoring?', verbose_name='Monitoring Lab Check Interval')),
                ('urgent_lab_interval', models.DurationField(default=datetime.timedelta(days=14), help_text='How frequently do you recheck urgent labs?', verbose_name='Urgent Lab Check Interval')),
                ('titrating', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='Is this ULTPlan still in the titration phase?')),
                ('last_titration', models.DateField(blank=True, help_text='When was the ULT dose last titrated?', null=True)),
                ('pause', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this ULTPlan on pause?')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical ult plan',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ULTPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('dose_adjustment', models.IntegerField(default=100, help_text='What is the dose adjustment for each titration for the chosen medication?', verbose_name='Dose Adjustment')),
                ('goal_urate', models.FloatField(default=6.0, help_text='What is the goal uric acid?', verbose_name='Goal Uric Acid')),
                ('titration_lab_interval', models.DurationField(default=datetime.timedelta(days=42), help_text='How frequently are labs required to be checked duration ULT titration?', verbose_name='Titration Lab Check Interval')),
                ('monitoring_lab_interval', models.DurationField(default=datetime.timedelta(days=180), help_text='How frequently are labs required to be checked during routine monitoring?', verbose_name='Monitoring Lab Check Interval')),
                ('urgent_lab_interval', models.DurationField(default=datetime.timedelta(days=14), help_text='How frequently do you recheck urgent labs?', verbose_name='Urgent Lab Check Interval')),
                ('titrating', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='Is this ULTPlan still in the titration phase?')),
                ('last_titration', models.DateField(blank=True, help_text='When was the ULT dose last titrated?', null=True)),
                ('pause', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this ULTPlan on pause?')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
