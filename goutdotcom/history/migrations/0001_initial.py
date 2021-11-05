# Generated by Django 3.1.7 on 2021-11-05 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='XOIInteractions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('date', models.DateField(blank=True, help_text='When did you start this medication?', null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on any medications that could interact with allopurinol or febuxostat? (6-mercaptopurine, azathioprine)?', null=True)),
                ('six_mp', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on 6-mercaptopurine / 6-MP?', null=True)),
                ('azathioprine', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on azathioprine / Imuran?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UrateKidneyStones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Have you had urate <a href='https://en.wikipedia.org/wiki/Kidney_stone_disease' target='_blank'>kidney stones</a>? If you don't know, skip this or leave it blank.", null=True, verbose_name='Urate Kidney Stones')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tophi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have gouty tophi?', null=True, verbose_name='Tophi')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('number', models.IntegerField(blank=True, default=1, help_text='How many have you had?', null=True)),
                ('date', models.DateField(blank=True, help_text='When was it? The most recent if multiple.', null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Have you ever had <a href='https://en.wikipedia.org/wiki/Stroke' target='_blank'>stroke</a>? If you don't know, skip this or leave it blank.", null=True, verbose_name='stroke')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shellfish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you eat a lot of shellfish?', null=True, verbose_name='shellfish')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganTransplant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('organ', multiselectfield.db.fields.MultiSelectField(choices=[('Heart', 'Heart'), ('Kidney', 'Kidney'), ('Liver', 'Liver'), ('Lung', 'Lung'), ('Pancreas', 'Pancreas'), ('Face', 'Face')], default=True, help_text='Which organ did you have transplanted?', max_length=37, null=True, verbose_name='Organ(s) transplanted')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Have you had an organ transplant?', null=True, verbose_name='Organ transplant')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hyperuricemia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have a history of elevated levels (> 9.0 mg/dL) of uric acid in your blood?', null=True, verbose_name='Hyperuricemia')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('medication', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Are you on <a href='https://www.heart.org/en/health-topics/high-blood-pressure/changes-you-can-make-to-manage-high-blood-pressure/types-of-blood-pressure-medications' target='_blank'>medications</a> for high blood pressure? If you don't know, skip this or leave it blank.", null=True, verbose_name='Blood pressure medications')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Do you have <a href='https://en.wikipedia.org/wiki/Hypertension' target='_blank'>hypertension</a>?", null=True, verbose_name='Hypertension (high blood pressure)')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('number', models.IntegerField(blank=True, default=1, help_text='How many have you had?', null=True)),
                ('date', models.DateField(blank=True, help_text='When was it? The most recent if multiple.', null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Have you ever had <a href='https://en.wikipedia.org/wiki/Myocardial_infarction' target='_blank'>heart attack</a>? If you don't know, skip this or leave it blank.", null=True, verbose_name='heart attack')),
                ('stent', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Have you had one or more <a href='https://en.wikipedia.org/wiki/Stent' target='_blank'>stent</a> placed? If you don't know, skip this or leave it blank.", null=True, verbose_name='stent')),
                ('stent_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='When was the last time you has a stent?', null=True)),
                ('cabg', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Have you had <a href='https://en.wikipedia.org/wiki/Coronary_artery_bypass_surgery' target='_blank'>bypass</a>? If you don't know, skip this or leave it blank.", null=True, verbose_name='cabg')),
                ('cabg_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='When did you have a bypass?', null=True)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('family_member', multiselectfield.db.fields.MultiSelectField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Sister', 'Sister'), ('Brother', 'Brother'), ('Uncle', 'Uncle'), ('Aunt', 'Aunt'), ('Son', 'Son'), ('Daughter', 'Daughter'), ('Grandpa', 'Grandpa'), ('Grandma', 'Grandma')], default=True, help_text='Which family members had family history?', max_length=68, null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have a family history of gout?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fructose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you eat a lot of fructose such as the sugar found in soda/pop, processed candies, or juices?', null=True, verbose_name='fructose')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Erosions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have erosions on your x-rays?', null=True, verbose_name='Erosions')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have a history?', null=True)),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('type', models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two')], help_text="Do you have <a href='https://en.wikipedia.org/wiki/Type_1_diabetes' target='_blank'>type I</a> or <a href='https://en.wikipedia.org/wiki/Type_2_diabetes' target='_blank'>type II</a> diabetes? If you don't know, skip this or leave it blank.", null=True, verbose_name='Type 1 or type 2 diabetes?')),
                ('insulin', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Are you on <a href='https://en.wikipedia.org/wiki/Insulin' target='_blank'>kidney stones</a>? If you don't know, skip this or leave it blank.", null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Do you have <a href='https://en.wikipedia.org/wiki/Diabetes' target='_blank'>diabetes</a>? If you don't know, skip this or leave it blank.", null=True, verbose_name='Diabetes')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
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
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you have a history?', null=True)),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('date', models.DateField(blank=True, help_text='When did you start this medication?', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ColchicineInteractions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('date', models.DateField(blank=True, help_text='When did you start this medication?', null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on any medications that could interact with colchicine? (clarithromycin, simvastatin, diltiazem)', null=True)),
                ('clarithromycin', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on clarithromycin', null=True)),
                ('simvastatin', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on simvastatin?', null=True)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('stage', models.IntegerField(blank=True, choices=[(1, 'I'), (2, 'Ii'), (3, 'Iii'), (4, 'Iv'), (5, 'V')], help_text="What <a href='https://www.kidney.org/sites/default/files/01-10-7278_HBG_CKD_Stages_Flyer_GFR.gif' target='_blank'>stage</a> is your CKD?? If you don't know, you probably aren't.", null=True, verbose_name='CKD stage')),
                ('dialysis', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Are you on <a href='https://en.wikipedia.org/wiki/Hemodialysis' target='_blank'>dialysis</a>? If you don't know, you probably aren't.", null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Do you have CKD (<a href='https://en.wikipedia.org/wiki/Chronic_kidney_disease' target='_blank'>chronic kidney disease</a>)? If you don't know, skip this or leave it blank.", null=True, verbose_name='Chronic Kidney Disease (CKD)')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('systolic', models.BooleanField(blank=True, choices=[(True, 'Systolic'), (False, 'Diastolic')], help_text="Do you have systolic (reduced <a href='https://en.wikipedia.org/wiki/Ejection_fraction' target='_blank'>ejection fraction</a>) heart failure? If you don't know, skip this or leave it blank.", null=True, verbose_name='Systolic or diastolic heart failure')),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Do you have CHF (<a href='https://en.wikipedia.org/wiki/Heart_failure' target='_blank'>congestive heart failure</a>)? If you don't know, skip this or leave it blank.", null=True, verbose_name='Congestive Heart Failure (CHF)')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bleed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('number', models.IntegerField(blank=True, default=1, help_text='How many have you had?', null=True)),
                ('date', models.DateField(blank=True, help_text='When was it? The most recent if multiple.', null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Have you ever had a major bleed?', null=True, verbose_name='major bleed')),
                ('GIB', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Have you ever had <a href='https://en.wikipedia.org/wiki/Gastrointestinal_bleeding' target='_blank'>gastrointestinal bleeding</a>? If you don't know, skip this or leave it blank.", null=True)),
                ('GIB_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='When was the last time you has a gastrointestinal bleed?', null=True)),
                ('CNS', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Have you had an intracranial bleed?', null=True)),
                ('CNS_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='When was the last time you had an intracranial bleed?', null=True)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('date', models.DateField(blank=True, help_text='When did you start this medication?', null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on anticoagulation?', null=True)),
                ('apixaban', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on apixaban / Eliquis?', null=True)),
                ('clopidogrel', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on clopidogrel / Plavix?', null=True)),
                ('dabigatran', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on dabigatran / Pradaxa?', null=True)),
                ('enoxaparin', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on enoxaparin / Lovenox?', null=True)),
                ('rivaroxaban', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on rivaroxaban / Xarelto?', null=True)),
                ('warfarin', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Are you on warfarin / Coumadin?', null=True)),
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
                ('last_modified', models.CharField(blank=True, choices=[('ContraindicationsProfile', 'ContraindicationsProfile'), ('FlareAid', 'FlareAid'), ('FlareDiagnosis', 'FlareDiagnosis'), ('FamilyProfile', 'FamilyProfile'), ('MedicalProfile', 'MedicalProfile'), ('SocialProfile', 'SocialProfile'), ('ULT', 'ULT'), ('ULTAid', 'ULTAid')], max_length=75, null=True)),
                ('value', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text='Do you drink alcohol?', null=True, verbose_name='alcohol')),
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
