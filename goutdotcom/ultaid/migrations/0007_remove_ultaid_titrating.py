# Generated by Django 3.1.7 on 2021-12-21 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultaid', '0006_ultaid_titrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ultaid',
            name='titrating',
        ),
    ]