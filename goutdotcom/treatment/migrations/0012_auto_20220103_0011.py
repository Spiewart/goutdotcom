# Generated by Django 3.1.7 on 2022-01-03 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0011_allopurinolhistory_de_sensitized'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='febuxostathistory',
            name='febuxostat',
        ),
        migrations.RemoveField(
            model_name='febuxostathistory',
            name='ultplan',
        ),
        migrations.RemoveField(
            model_name='febuxostathistory',
            name='user',
        ),
        migrations.RemoveField(
            model_name='probenecidhistory',
            name='probenecid',
        ),
        migrations.RemoveField(
            model_name='probenecidhistory',
            name='ultplan',
        ),
        migrations.RemoveField(
            model_name='probenecidhistory',
            name='user',
        ),
        migrations.DeleteModel(
            name='AllopurinolHistory',
        ),
        migrations.DeleteModel(
            name='FebuxostatHistory',
        ),
        migrations.DeleteModel(
            name='ProbenecidHistory',
        ),
    ]
