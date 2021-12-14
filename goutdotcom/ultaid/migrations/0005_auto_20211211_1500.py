# Generated by Django 3.1.7 on 2021-12-11 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultaid', '0004_auto_20211210_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ultaid',
            name='need',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text="Do you need <a href='/ult/create/' target='_blank'>ULT</a>?", verbose_name='Need ULT?'),
        ),
        migrations.AlterField(
            model_name='ultaid',
            name='want',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text='Will you take daily medication to get rid of your gout?', verbose_name='Want ULT?'),
        ),
    ]