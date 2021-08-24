# Generated by Django 3.1.7 on 2021-08-11 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ult', '0008_auto_20210811_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ult',
            name='first_flare',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text='If so, disregard the rest of the questions.', verbose_name='Are you having your first flare?'),
        ),
        migrations.AlterField(
            model_name='ult',
            name='num_flares',
            field=models.CharField(choices=[('zero', 'Zero'), ('one', 'One'), ('1-3', '2-3'), ('4-6', '4-6'), ('7 or more', '7 or more')], default='one', help_text='An estimate is fine!', max_length=30, verbose_name='Approximately how many gout flares have you had?'),
        ),
    ]