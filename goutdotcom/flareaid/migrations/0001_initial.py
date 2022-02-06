# Generated by Django 3.1.7 on 2022-02-05 14:58

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlareAid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('perfect_health', models.BooleanField(blank=True, choices=[('', '-----'), (True, 'Yes'), (False, 'No')], default='', help_text='Meaning no chronic medical problems', null=True, verbose_name='Besides having gout, are you in perfect health?')),
                ('monoarticular', models.BooleanField(blank=True, choices=[('', '-----'), (True, 'Yes'), (False, 'No')], default='', help_text='Meaning just a toe, knee, etc.', null=True, verbose_name='Is your flare in just a single joint?')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
