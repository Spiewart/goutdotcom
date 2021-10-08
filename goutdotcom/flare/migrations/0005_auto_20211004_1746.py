# Generated by Django 3.1.7 on 2021-10-04 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0003_auto_20211004_1509'),
        ('flare', '0004_decisionaid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decisionaid',
            name='diabetes',
            field=models.ForeignKey(blank=True, help_text='Type I or type II', null=True, on_delete=django.db.models.deletion.CASCADE, to='history.diabetes', verbose_name='Do you have diabetes?'),
        ),
    ]
