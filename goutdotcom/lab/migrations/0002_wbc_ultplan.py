# Generated by Django 3.1.7 on 2022-01-29 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ultplan', '0001_initial'),
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wbc',
            name='ultplan',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ultplan.ultplan'),
        ),
    ]
