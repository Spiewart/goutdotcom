# Generated by Django 3.1.7 on 2022-01-12 21:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0003_auto_20220112_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allopurinol',
            name='dose',
            field=models.IntegerField(choices=[(50, '50 mg'), (100, '100 mg'), (150, '150 mg'), (200, '200 mg'), (250, '250 mg'), (300, '300 mg'), (350, '350 mg'), (400, '400 mg'), (450, '450 mg'), (500, '500 mg'), (550, '550 mg'), (600, '600 mg'), (650, '650 mg'), (700, '700 mg'), (750, '750 mg'), (800, '800 mg'), (850, '850 mg'), (900, '900 mg')], default=100, validators=[django.core.validators.MaxValueValidator(750), django.core.validators.MinValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='febuxostat',
            name='dose',
            field=models.IntegerField(choices=[(20, '20 mg'), (40, '40 mg'), (60, '60 mg'), (80, '80 mg'), (100, '100 mg'), (120, '120 mg')], default=40, validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(20)]),
        ),
        migrations.AlterField(
            model_name='probenecid',
            name='dose',
            field=models.IntegerField(choices=[(250, '250 mg'), (500, '500 mg'), (750, '750 mg'), (1000, '1000 mg')], validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(250)]),
        ),
    ]
