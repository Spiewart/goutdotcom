# Generated by Django 3.1.7 on 2022-01-29 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ultaid', '0001_initial'),
        ('ultplan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ultaid',
            name='ultplan',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ultplan.ultplan'),
        ),
    ]
