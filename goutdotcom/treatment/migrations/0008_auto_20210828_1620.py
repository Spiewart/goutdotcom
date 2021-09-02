# Generated by Django 3.1.7 on 2021-08-28 16:20

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0007_auto_20210828_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celecoxib',
            name='dose',
            field=models.IntegerField(blank=True, choices=[(200, '200 mg'), (400, '400 mg')], null=True),
        ),
        migrations.AlterField(
            model_name='colchicine',
            name='dose',
            field=models.DecimalField(blank=True, choices=[(Decimal('0.6'), '0.6 mg')], decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='meloxicam',
            name='dose',
            field=models.DecimalField(blank=True, choices=[(Decimal('7.5'), '7.5 mg'), (Decimal('15'), '15 mg')], decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='methylprednisolone',
            name='dose',
            field=models.IntegerField(blank=True, choices=[(20, '20 mg'), (40, '40 mg'), (80, '80 mg')], null=True),
        ),
        migrations.AlterField(
            model_name='naproxen',
            name='dose',
            field=models.IntegerField(blank=True, choices=[(220, '220 mg'), (250, '250 mg'), (440, '440 mg'), (500, '500 mg')], null=True),
        ),
        migrations.AlterField(
            model_name='othertreat',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='prednisone',
            name='dose',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tinctureoftime',
            name='duration',
            field=models.IntegerField(blank=True, help_text='How long did it take to get better?', null=True),
        ),
    ]