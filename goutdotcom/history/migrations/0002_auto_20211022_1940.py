# Generated by Django 3.1.7 on 2021-10-22 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chf',
            name='systolic',
            field=models.BooleanField(blank=True, choices=[(True, 'Systolic'), (False, 'Diastolic')], help_text="Do you have systolic (reduced ejection fraction) heart faliure? If you don't know, skip this or leave it blank.", null=True, verbose_name='Systolic or diastolic heart failure'),
        ),
    ]