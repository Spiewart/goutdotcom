# Generated by Django 3.1.7 on 2021-12-07 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flare', '0008_auto_20211203_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flare',
            name='duration',
            field=models.CharField(blank=True, choices=[('more than 3 but less than 7 days', 'More than 3 but less than 7 days'), ('more than 1 but less than 3 days', 'More than 1 but less than 3 days'), ('under 24 hours', 'Under 24 hours'), ('over 14 days', 'Over 14 days'), ('more than 7 but less than 10 days', 'More than 7 but less than 10 days'), ('more than 10 but less than 14 days', 'More than 10 but less than 14 days')], help_text='How long did your symptoms last?', max_length=60, null=True, verbose_name='Symptom Duration'),
        ),
    ]
