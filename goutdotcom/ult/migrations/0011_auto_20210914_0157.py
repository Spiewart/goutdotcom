# Generated by Django 3.1.7 on 2021-09-14 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ult', '0010_auto_20210814_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ult',
            name='num_flares',
            field=models.CharField(blank=True, choices=[('zero', 'Zero'), ('one', 'One'), ('1-3', '2-3'), ('4-6', '4-6'), ('7 or more', '7 or more')], default='', help_text='If more than one, an estimate is fine!', max_length=30, null=True, verbose_name='How many gout flares have you had?'),
        ),
    ]