# Generated by Django 3.1.7 on 2021-07-26 18:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date_drawn', models.DateTimeField(default=django.utils.timezone.now, help_text='What day was this lab drawn?')),
                ('value', models.IntegerField(blank=True, help_text='Enter your weight in pounds', null=True, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(600)])),
                ('units', models.CharField(blank=True, choices=[('inches', 'inches'), ('meters', 'meters'), ('pounds', 'pounds'), ('kilos', 'kilograms'), ('mm (milimeters) of mercury', 'mm (milimeters) of mercury'), ('degrees Farenheit', 'degrees Farenheit'), ('degrees Celsius', 'degrees Celsius'), ('beats per minute', 'beats per minute'), ('breaths per minute', 'breaths per minute')], default='pounds', max_length=100, null=True)),
                ('altunit', models.CharField(blank=True, choices=[('inches', 'inches'), ('meters', 'meters'), ('pounds', 'pounds'), ('kilos', 'kilograms'), ('mm (milimeters) of mercury', 'mm (milimeters) of mercury'), ('degrees Farenheit', 'degrees Farenheit'), ('degrees Celsius', 'degrees Celsius'), ('beats per minute', 'beats per minute'), ('breaths per minute', 'breaths per minute')], default='kilos', max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]