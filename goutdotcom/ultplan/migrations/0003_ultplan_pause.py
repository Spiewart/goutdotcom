# Generated by Django 3.1.7 on 2022-01-18 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultplan', '0002_ultplan_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ultplan',
            name='pause',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this ULTPlan on pause?'),
        ),
    ]