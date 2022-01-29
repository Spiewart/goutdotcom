# Generated by Django 3.1.7 on 2022-01-29 20:42

from django.db import migrations, models
import django_extensions.db.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('monoarticular', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Does your gout flare involve only 1 joint?', null=True, verbose_name='Monoarticular')),
                ('male', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Are you male (biologically from birth or medically after birth)?', null=True, verbose_name='Male?')),
                ('prior_gout', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Have you had a prior <a href='/flare/about/' target='_blank'>gout flare</a>or other sudden onset arthritis attack consistent with gout?", null=True, verbose_name='Prior Gout Flare')),
                ('onset', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Did your symptoms start and reach maximum intensity within 1 day?', null=True, verbose_name='Rapid Onset (1 day)')),
                ('redness', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is(are) the joint(s) red (erythematous)?', null=True, verbose_name='Redness')),
                ('firstmtp', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is the ', null=True, verbose_name='Is your big toe the painful joint?')),
                ('location', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Right foot', 'Right foot'), ('Left foot', 'Left foot'), ('Right ankle', 'Right ankle'), ('Left ankle', 'Left ankle'), ('Right knee', 'Right knee'), ('Left knee', 'Left knee'), ('Right hip', 'Right hip'), ('Left hip', 'Left hip'), ('Right hand', 'Right hand'), ('Left hand', 'Left hand'), ('Right wrist', 'Right wrist'), ('Left wrist', 'Left wrist'), ('Right elbow', 'Right elbow'), ('Left elbow', 'Left elbow'), ('Right shoulder', 'Right shoulder'), ('Left shoulder', 'Left shoulder')], help_text='What joint did the flare occur in?', max_length=179, null=True)),
                ('duration', models.CharField(blank=True, choices=[('under 24 hours', 'Under 24 hours'), ('more than 1 but less than 3 days', 'More than 1 but less than 3 days'), ('more than 3 but less than 7 days', 'More than 3 but less than 7 days'), ('more than 7 but less than 10 days', 'More than 7 but less than 10 days'), ('more than 10 but less than 14 days', 'More than 10 but less than 14 days'), ('over 14 days', 'Over 14 days')], help_text='How long did your symptoms last?', max_length=60, null=True, verbose_name='Symptom Duration')),
                ('treatment', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Colcrys', 'Colchicine'), ('Advil', 'Ibuprofen'), ('Aleve', 'Naproxen'), ('Celebrex', 'Celecoxib'), ('Indocin', 'Indocin'), ('Mobic', 'Meloxicam'), ('Prednisone', 'Prednisone'), ('Methylprednisolone', 'Methylprednisolone'), ('Tincture of time', 'Tincture of time'), ('Other treatment', 'Other treatment')], help_text='What was the flare treated with?', max_length=105, null=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
