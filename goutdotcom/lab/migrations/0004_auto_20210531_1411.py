# Generated by Django 3.1.7 on 2021-05-31 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0003_auto_20210427_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urate',
            name='uric_acid',
            field=models.DecimalField(blank=True, decimal_places=1, help_text='Enter the uric acid', max_digits=3, null=True),
        ),
    ]