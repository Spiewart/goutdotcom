# Generated by Django 3.1.7 on 2022-03-13 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('history', '0002_auto_20220313_2025'),
        ('ppxaid', '0001_initial'),
        ('ultplan', '0001_initial'),
        ('ultaid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ppxaid',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ppxaid_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ppxaid',
            name='diabetes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.diabetes'),
        ),
        migrations.AddField(
            model_name='ppxaid',
            name='heartattack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.heartattack'),
        ),
        migrations.AddField(
            model_name='ppxaid',
            name='ibd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.ibd'),
        ),
        migrations.AddField(
            model_name='ppxaid',
            name='osteoporosis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.osteoporosis'),
        ),
        migrations.AddField(
            model_name='ppxaid',
            name='stroke',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.stroke'),
        ),
        migrations.AddField(
            model_name='ppxaid',
            name='ultaid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ultaid.ultaid'),
        ),
        migrations.AddField(
            model_name='ppxaid',
            name='ultplan',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ultplan.ultplan'),
        ),
        migrations.AddField(
            model_name='ppxaid',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]