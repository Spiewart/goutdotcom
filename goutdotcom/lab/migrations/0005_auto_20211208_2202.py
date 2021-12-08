# Generated by Django 3.1.7 on 2021-12-08 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_auto_20211207_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urate',
            name='value',
            field=models.DecimalField(decimal_places=1, help_text='Typically reported in mg/dL', max_digits=3),
        ),
    ]
