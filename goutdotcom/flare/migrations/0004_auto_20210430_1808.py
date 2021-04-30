# Generated by Django 3.1.7 on 2021-04-30 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flare', '0003_flare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flare',
            name='treatment',
            field=models.CharField(choices=[('Colcrys', 'Colchicine'), ('Advil', 'Ibuprofen'), ('Aleve', 'Naproxen'), ('Celebrex', 'Celecoxib'), ('Mobic', 'Meloxicam'), ('Pred', 'Prednisone'), ('Methylpred', 'Methylprednisolone'), ('Tincture of time', 'Tincture of time'), ('Other', 'Other')], help_text='What was the flare treated with?', max_length=60),
        ),
    ]
