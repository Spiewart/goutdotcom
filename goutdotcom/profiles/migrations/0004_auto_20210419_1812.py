# Generated by Django 3.1.7 on 2021-04-19 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210419_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='age',
            field=models.IntegerField(blank=True, default=35, help_text='Enter age', null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='height',
            field=models.IntegerField(blank=True, help_text='How tall are you in feet/inches?', null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='weight',
            field=models.IntegerField(blank=True, help_text='How much do you weight in pounds?', null=True),
        ),
    ]
