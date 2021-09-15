# Generated by Django 3.1.7 on 2021-09-15 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_colchicineinteractions_organtransplant_xoiinteractions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ckd',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have CKD?', null=True, verbose_name='Chronic kidney disease (CKD)'),
        ),
    ]
