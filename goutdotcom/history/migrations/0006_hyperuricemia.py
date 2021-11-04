# Generated by Django 3.1.7 on 2021-10-25 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('history', '0005_auto_20211024_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hyperuricemia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have a history of elevated levels of uric acid in your blood?', null=True, verbose_name='Do you have blood uric acid levels greater than 9.0 mg/dL?')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
