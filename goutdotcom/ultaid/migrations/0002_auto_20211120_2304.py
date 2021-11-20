# Generated by Django 3.1.7 on 2021-11-20 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultaid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ultaid',
            name='need',
            field=models.BooleanField(blank=True, choices=[('', '-----'), (True, 'Yes'), (False, 'No')], default='', help_text="Do you need <a href='{% url 'ult:create' %}' target='_blank'>ULT</a>?", null=True, verbose_name='Need ULT?'),
        ),
        migrations.AddField(
            model_name='ultaid',
            name='want',
            field=models.BooleanField(blank=True, choices=[('', '-----'), (True, 'Yes'), (False, 'No')], default='', help_text='Will you take daily medication to get rid of your gout?', null=True, verbose_name='Want ULT?'),
        ),
    ]
