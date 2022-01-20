# Generated by Django 3.1.7 on 2022-01-18 17:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ultplan', '0003_ultplan_pause'),
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
                ('titrating', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='Is this ULTPlan still in the titration phase?')),
                ('last_titration', models.DateField(blank=True, help_text='When was the ULT dose last titrated?', null=True)),
                ('pause', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this ULTPlan on pause?')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical ult plan',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
