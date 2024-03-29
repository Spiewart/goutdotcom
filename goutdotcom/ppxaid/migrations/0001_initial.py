# Generated by Django 3.1.7 on 2022-03-13 20:25

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PPxAid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('perfect_health', models.BooleanField(blank=True, choices=[('', '-----'), (True, 'Yes'), (False, 'No')], default='', help_text='Meaning no chronic medical problems', null=True, verbose_name='Besides having gout, are you in perfect health?')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('anticoagulation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.anticoagulation')),
                ('bleed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.bleed')),
                ('ckd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.ckd')),
                ('colchicine_interactions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.colchicineinteractions')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
