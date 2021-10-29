# Generated by Django 3.1.7 on 2021-10-24 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flareaid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flareaid',
            name='perfect_health',
            field=models.BooleanField(blank=True, choices=[('', '-----'), (True, 'Yes'), (False, 'No')], default='', help_text='Meaning no chronic medical problems', null=True, verbose_name='Besides having gout, are you in perfect health?'),
        ),
    ]
