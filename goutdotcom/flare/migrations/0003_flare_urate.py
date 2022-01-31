# Generated by Django 3.1.7 on 2022-01-29 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lab', '0001_initial'),
        ('flare', '0002_auto_20220129_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='flare',
            name='urate',
            field=models.OneToOneField(blank=True, help_text='Did you get your uric acid checked at the time of your flare?', null=True, on_delete=django.db.models.deletion.CASCADE, to='lab.urate'),
        ),
    ]
