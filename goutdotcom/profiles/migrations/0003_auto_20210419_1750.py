# Generated by Django 3.1.7 on 2021-04-19 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20210419_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='age',
            field=models.IntegerField(blank=True, default=35, help_text='Enter age', null=True, verbose_name=range(0, -149)),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='drinks_per_week',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female'), ('non-binary', 'non-binary')], help_text='Enter gender', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='height',
            field=models.IntegerField(blank=True, help_text='How tall are you in feet/inches?', null=True, verbose_name=range(0, -100)),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='race',
            field=models.CharField(blank=True, choices=[('white', 'white'), ('black', 'black'), ('asian', 'asian'), ('native american', 'native american'), ('hispanic', 'hispanic')], help_text='Enter race', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='weight',
            field=models.IntegerField(blank=True, help_text='How much do you weight in pounds?', null=True, verbose_name=range(0, -950)),
        ),
    ]