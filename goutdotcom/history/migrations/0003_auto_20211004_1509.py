# Generated by Django 3.1.7 on 2021-10-04 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_auto_20211004_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erosions',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have a history of erosions?', null=True, verbose_name='Do you have erosions on your x-rays?'),
        ),
        migrations.AlterField(
            model_name='tophi',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have a history of tophi?', null=True, verbose_name='Do you have tophi on your x-rays?'),
        ),
    ]
