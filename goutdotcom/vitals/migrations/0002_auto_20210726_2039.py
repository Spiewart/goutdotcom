# Generated by Django 3.1.7 on 2021-07-26 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vitals', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weight',
            old_name='date_drawn',
            new_name='date_recorded',
        ),
    ]