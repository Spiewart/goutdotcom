# Generated by Django 3.1.7 on 2022-02-05 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ultplan', '0001_initial'),
        ('ppxaid', '0002_ppxaid_ultaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ppxaid',
            name='ultplan',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ultplan.ultplan'),
        ),
    ]
