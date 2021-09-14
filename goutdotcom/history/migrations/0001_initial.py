# Generated by Django 3.1.7 on 2021-09-14 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UrateKidneyStones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stroke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('number', models.IntegerField(blank=True, default=1, help_text='How many have you had?', null=True)),
                ('date', models.DateField(blank=True, help_text='When was it? The most recent if multiple.', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hypertension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('medication', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on medications for high blood pressure?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HeartAttack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('number', models.IntegerField(blank=True, default=1, help_text='How many have you had?', null=True)),
                ('date', models.DateField(blank=True, help_text='When was it? The most recent if multiple.', null=True)),
                ('stent', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Have you had stents placed?', null=True)),
                ('cabg', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Have you had bypass?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have a family history of family history?', null=True)),
                ('family_member', multiselectfield.db.fields.MultiSelectField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Sister', 'Sister'), ('Brother', 'Brother'), ('Uncle', 'Uncle'), ('Aunt', 'Aunt'), ('Son', 'Son'), ('Daughter', 'Daughter'), ('Grandpa', 'Grandpa'), ('Grandma', 'Grandma')], default=True, help_text='Which family members had family history?', max_length=68, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Diuretics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('date', models.DateField(blank=True, help_text='When did you start this medication?', null=True)),
                ('hydrochlorothiazide', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on hydrochlorothiazide?', null=True)),
                ('furosemide', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on Lasix / furosemide?', null=True)),
                ('bumetanide', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on Bumex / bumetanide?', null=True)),
                ('torsemide', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on torsemide?', null=True)),
                ('metolazone', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on metolazone?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Diabetes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('type', models.IntegerField(blank=True, choices=[(1, 'I'), (2, 'Ii')], help_text='Do you have type I or type II diabetes?', null=True)),
                ('insulin', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on insulin?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cyclosporine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('date', models.DateField(blank=True, help_text='When did you start this medication?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CKD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('stage', models.IntegerField(blank=True, choices=[(1, 'I'), (2, 'Ii'), (3, 'Iii'), (4, 'Iv'), (5, 'V')], help_text='What stage?', null=True)),
                ('dialysis', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on dialysis?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CHF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('systolic', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have systolic (reduced ejection fraction) heart faliure?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BleedingEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('number', models.IntegerField(blank=True, default=1, help_text='How many have you had?', null=True)),
                ('date', models.DateField(blank=True, help_text='When was it? The most recent if multiple.', null=True)),
                ('GIB', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Have you had a gastrointestinal bleed?', null=True)),
                ('CNS', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Have you had an intracranial bleed?', null=True)),
                ('transfusion', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Did you require a transfusion?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Anticoagulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date', models.DateField(blank=True, help_text='When did you start this medication?', null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on anticoagulation?', null=True)),
                ('warfarin', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on warfarin / Coumadin?', null=True)),
                ('apixaban', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on apixaban / Eliquis?', null=True)),
                ('rivaroxaban', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on rivaroxaban / Xarelto?', null=True)),
                ('clopidogrel', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on clopidogrel / Plavix?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Alcohol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have history?', null=True)),
                ('number', models.IntegerField(blank=True, help_text='How many drinks do you have per week?', null=True)),
                ('wine', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you drink wine?', null=True)),
                ('beer', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you drink beer?', null=True)),
                ('liquor', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you drink liquor?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
