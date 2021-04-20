# Generated by Django 3.1.7 on 2021-04-12 17:53

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ULT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('num_flares', models.CharField(choices=[('zero', 'Zero'), ('one', 'One'), ('1-3', '1-3'), ('4-6', '4-6'), ('7 or more', '7 or more')], help_text='Approximately how many gout flares have you had?', max_length=30)),
                ('freq_flares', models.CharField(choices=[('Under two', 'Under two'), ('Greater than two', 'Greater than two')], help_text='Approximately how often do you have flares?', max_length=30)),
                ('first_flare', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text='Is this your first flare?')),
                ('erosions', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text="Do you have erosions on your x-rays? If you don't know, that's OK!")),
                ('tophi', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text="Do you have tophi? If you don't know, that's OK!")),
                ('stones', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text="Have you ever had kidney stones made of uric acid? If you don't know, that's OK!")),
                ('ckd', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text="Do you have chronic kidney disease (CKD)? If you don't know, that's OK!")),
                ('uric_acid', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text="Is your uric acid over 9.0? If you don't know, that's OK!")),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]