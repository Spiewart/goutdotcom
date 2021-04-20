# Generated by Django 3.1.7 on 2021-04-20 15:54

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_patientprofile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='user__username', unique=True, verbose_name='User Profile'),
        ),
    ]
