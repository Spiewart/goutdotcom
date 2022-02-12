# Generated by Django 3.1.7 on 2022-02-12 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ultaid', '0003_ultaid_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ultaid',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ultaid_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
