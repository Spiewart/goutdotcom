# Generated by Django 3.1.7 on 2021-04-20 20:00

import autoslug.fields
import datetime
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Naproxen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date_started', models.DateField(default=datetime.datetime.now)),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('freq', models.CharField(choices=[('qday', 'Once daily'), ('bid', 'Twice daily'), ('tid', 'Three times daily'), ('qday prn', 'Once daily as needed'), ('bid prn', 'Twice daily as needed'), ('q2weeks', 'Every 2 weeks')], default='qday', max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user__username', unique=True, verbose_name='Patient')),
                ('generic_name', models.CharField(choices=[('allopurinol', 'Allopurinol'), ('febuxostat', 'Febuxostat'), ('prednisone', 'Prednisone'), ('colchicine', 'Colchicine'), ('probenacid', 'Probenacid'), ('pegloticase', 'Pegloticase'), ('ibuprofen', 'Ibuprofen'), ('naproxen', 'Naproxen'), ('meloxicam', 'Meloxicam'), ('celecoxib', 'Celecoxib')], default='naproxen', max_length=60)),
                ('med_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='generic_name', unique=True, verbose_name='Medication Name')),
                ('dose', models.IntegerField(choices=[('220', '220 mg'), ('250', '250 mg'), ('440', '440 mg'), ('500', '500 mg')])),
                ('side_effects', models.CharField(blank=True, choices=[('Rash', 'Rash'), ('Kidney failure', 'Kidney failure'), ('Stomach ulcer', 'Stomach ulcer'), ('GI upset', 'GI upset'), ('Medication interaction', 'Medication interaction')], help_text='Have you had any side effects?', max_length=100, null=True)),
                ('drug_class', models.CharField(choices=[('urate-lowering therapy', 'Urate-lowering therapy'), ('systemic steroid', 'Systemic steroid'), ('anti-inflammatory', 'Anti-inflammatory'), ('nonsteroidal antiinflammatory drug', 'Nonsteroidal anti-inflammatory drug'), ('urate extreagogue', 'Urate excretagogue'), ('local steroid', 'Local steroid'), ('recombinant uricase', 'Recombinant uricase')], default='nonsteroidal antiinflammatory drug', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meloxicam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date_started', models.DateField(default=datetime.datetime.now)),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('freq', models.CharField(choices=[('qday', 'Once daily'), ('bid', 'Twice daily'), ('tid', 'Three times daily'), ('qday prn', 'Once daily as needed'), ('bid prn', 'Twice daily as needed'), ('q2weeks', 'Every 2 weeks')], default='qday', max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user__username', unique=True, verbose_name='Patient')),
                ('generic_name', models.CharField(choices=[('allopurinol', 'Allopurinol'), ('febuxostat', 'Febuxostat'), ('prednisone', 'Prednisone'), ('colchicine', 'Colchicine'), ('probenacid', 'Probenacid'), ('pegloticase', 'Pegloticase'), ('ibuprofen', 'Ibuprofen'), ('naproxen', 'Naproxen'), ('meloxicam', 'Meloxicam'), ('celecoxib', 'Celecoxib')], default='meloxicam', max_length=60)),
                ('med_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='generic_name', unique=True, verbose_name='Medication Name')),
                ('dose', models.IntegerField(choices=[('7.5', '7.5 mg'), ('15', '15 mg')])),
                ('side_effects', models.CharField(blank=True, choices=[('Rash', 'Rash'), ('Kidney failure', 'Kidney failure'), ('Stomach ulcer', 'Stomach ulcer'), ('GI upset', 'GI upset'), ('Medication interaction', 'Medication interaction')], help_text='Have you had any side effects?', max_length=100, null=True)),
                ('drug_class', models.CharField(choices=[('urate-lowering therapy', 'Urate-lowering therapy'), ('systemic steroid', 'Systemic steroid'), ('anti-inflammatory', 'Anti-inflammatory'), ('nonsteroidal antiinflammatory drug', 'Nonsteroidal anti-inflammatory drug'), ('urate extreagogue', 'Urate excretagogue'), ('local steroid', 'Local steroid'), ('recombinant uricase', 'Recombinant uricase')], default='nonsteroidal antiinflammatory drug', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ibuprofen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date_started', models.DateField(default=datetime.datetime.now)),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('freq', models.CharField(choices=[('qday', 'Once daily'), ('bid', 'Twice daily'), ('tid', 'Three times daily'), ('qday prn', 'Once daily as needed'), ('bid prn', 'Twice daily as needed'), ('q2weeks', 'Every 2 weeks')], default='qday', max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user__username', unique=True, verbose_name='Patient')),
                ('generic_name', models.CharField(choices=[('allopurinol', 'Allopurinol'), ('febuxostat', 'Febuxostat'), ('prednisone', 'Prednisone'), ('colchicine', 'Colchicine'), ('probenacid', 'Probenacid'), ('pegloticase', 'Pegloticase'), ('ibuprofen', 'Ibuprofen'), ('naproxen', 'Naproxen'), ('meloxicam', 'Meloxicam'), ('celecoxib', 'Celecoxib')], default='ibuprofen', max_length=60)),
                ('med_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='generic_name', unique=True, verbose_name='Medication Name')),
                ('dose', models.IntegerField(choices=[('200', '200 mg'), ('400', '400 mg'), ('600', '600 mg'), ('800', '800 mg')])),
                ('side_effects', models.CharField(blank=True, choices=[('Rash', 'Rash'), ('Kidney failure', 'Kidney failure'), ('Stomach ulcer', 'Stomach ulcer'), ('GI upset', 'GI upset'), ('Medication interaction', 'Medication interaction')], help_text='Have you had any side effects?', max_length=100, null=True)),
                ('drug_class', models.CharField(choices=[('urate-lowering therapy', 'Urate-lowering therapy'), ('systemic steroid', 'Systemic steroid'), ('anti-inflammatory', 'Anti-inflammatory'), ('nonsteroidal antiinflammatory drug', 'Nonsteroidal anti-inflammatory drug'), ('urate extreagogue', 'Urate excretagogue'), ('local steroid', 'Local steroid'), ('recombinant uricase', 'Recombinant uricase')], default='nonsteroidal antiinflammatory drug', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Febuxostat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date_started', models.DateField(default=datetime.datetime.now)),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('freq', models.CharField(choices=[('qday', 'Once daily'), ('bid', 'Twice daily'), ('tid', 'Three times daily'), ('qday prn', 'Once daily as needed'), ('bid prn', 'Twice daily as needed'), ('q2weeks', 'Every 2 weeks')], default='qday', max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user__username', unique=True, verbose_name='Patient')),
                ('generic_name', models.CharField(choices=[('allopurinol', 'Allopurinol'), ('febuxostat', 'Febuxostat'), ('prednisone', 'Prednisone'), ('colchicine', 'Colchicine'), ('probenacid', 'Probenacid'), ('pegloticase', 'Pegloticase'), ('ibuprofen', 'Ibuprofen'), ('naproxen', 'Naproxen'), ('meloxicam', 'Meloxicam'), ('celecoxib', 'Celecoxib')], default='febuxostat', max_length=60)),
                ('med_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='generic_name', unique=True, verbose_name='Medication Name')),
                ('dose', models.IntegerField(choices=[(20, '20 mg'), (40, '40 mg'), (60, '60 mg'), (80, '80 mg'), (100, '100 mg'), (120, '120 mg')])),
                ('side_effects', models.CharField(blank=True, choices=[('Rash', 'Rash'), ('Hypersensitivity syndrome', 'Hypersensitivity syndrome'), ('Elevated LFTs', 'Elevated LFTs'), ('Cytopenias', 'Cytopenias'), ('GI upset', 'GI upset')], help_text='Have you had any side effects?', max_length=100, null=True)),
                ('drug_class', models.CharField(choices=[('urate-lowering therapy', 'Urate-lowering therapy'), ('systemic steroid', 'Systemic steroid'), ('anti-inflammatory', 'Anti-inflammatory'), ('nonsteroidal antiinflammatory drug', 'Nonsteroidal anti-inflammatory drug'), ('urate extreagogue', 'Urate excretagogue'), ('local steroid', 'Local steroid'), ('recombinant uricase', 'Recombinant uricase')], default='urate-lowering therapy', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Colchicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date_started', models.DateField(default=datetime.datetime.now)),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('freq', models.CharField(choices=[('qday', 'Once daily'), ('bid', 'Twice daily'), ('tid', 'Three times daily'), ('qday prn', 'Once daily as needed'), ('bid prn', 'Twice daily as needed'), ('q2weeks', 'Every 2 weeks')], default='qday', max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user__username', unique=True, verbose_name='Patient')),
                ('generic_name', models.CharField(choices=[('allopurinol', 'Allopurinol'), ('febuxostat', 'Febuxostat'), ('prednisone', 'Prednisone'), ('colchicine', 'Colchicine'), ('probenacid', 'Probenacid'), ('pegloticase', 'Pegloticase'), ('ibuprofen', 'Ibuprofen'), ('naproxen', 'Naproxen'), ('meloxicam', 'Meloxicam'), ('celecoxib', 'Celecoxib')], default='colchicine', max_length=60)),
                ('med_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='generic_name', unique=True, verbose_name='Medication Name')),
                ('dose', models.IntegerField(choices=[(Decimal('0.6'), '0.6 mg')])),
                ('side_effects', models.CharField(blank=True, choices=[('GI upset', 'GI upset'), ('Medication interaction', 'Medication interaction')], help_text='Have you had any side effects?', max_length=100, null=True)),
                ('drug_class', models.CharField(choices=[('urate-lowering therapy', 'Urate-lowering therapy'), ('systemic steroid', 'Systemic steroid'), ('anti-inflammatory', 'Anti-inflammatory'), ('nonsteroidal antiinflammatory drug', 'Nonsteroidal anti-inflammatory drug'), ('urate extreagogue', 'Urate excretagogue'), ('local steroid', 'Local steroid'), ('recombinant uricase', 'Recombinant uricase')], default='anti-inflammatory', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CELECOXIB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date_started', models.DateField(default=datetime.datetime.now)),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('freq', models.CharField(choices=[('qday', 'Once daily'), ('bid', 'Twice daily'), ('tid', 'Three times daily'), ('qday prn', 'Once daily as needed'), ('bid prn', 'Twice daily as needed'), ('q2weeks', 'Every 2 weeks')], default='qday', max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user__username', unique=True, verbose_name='Patient')),
                ('generic_name', models.CharField(choices=[('allopurinol', 'Allopurinol'), ('febuxostat', 'Febuxostat'), ('prednisone', 'Prednisone'), ('colchicine', 'Colchicine'), ('probenacid', 'Probenacid'), ('pegloticase', 'Pegloticase'), ('ibuprofen', 'Ibuprofen'), ('naproxen', 'Naproxen'), ('meloxicam', 'Meloxicam'), ('celecoxib', 'Celecoxib')], default='celecoxib', max_length=60)),
                ('med_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='generic_name', unique=True, verbose_name='Medication Name')),
                ('dose', models.IntegerField(choices=[('200', '200 mg'), ('400', '400 mg')])),
                ('side_effects', models.CharField(blank=True, choices=[('Rash', 'Rash'), ('Kidney failure', 'Kidney failure'), ('Stomach ulcer', 'Stomach ulcer'), ('GI upset', 'GI upset'), ('Medication interaction', 'Medication interaction')], help_text='Have you had any side effects?', max_length=100, null=True)),
                ('drug_class', models.CharField(choices=[('urate-lowering therapy', 'Urate-lowering therapy'), ('systemic steroid', 'Systemic steroid'), ('anti-inflammatory', 'Anti-inflammatory'), ('nonsteroidal antiinflammatory drug', 'Nonsteroidal anti-inflammatory drug'), ('urate extreagogue', 'Urate excretagogue'), ('local steroid', 'Local steroid'), ('recombinant uricase', 'Recombinant uricase')], default='nonsteroidal antiinflammatory drug', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Allopurinol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date_started', models.DateField(default=datetime.datetime.now)),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('freq', models.CharField(choices=[('qday', 'Once daily'), ('bid', 'Twice daily'), ('tid', 'Three times daily'), ('qday prn', 'Once daily as needed'), ('bid prn', 'Twice daily as needed'), ('q2weeks', 'Every 2 weeks')], default='qday', max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user__username', unique=True, verbose_name='Patient')),
                ('generic_name', models.CharField(choices=[('allopurinol', 'Allopurinol'), ('febuxostat', 'Febuxostat'), ('prednisone', 'Prednisone'), ('colchicine', 'Colchicine'), ('probenacid', 'Probenacid'), ('pegloticase', 'Pegloticase'), ('ibuprofen', 'Ibuprofen'), ('naproxen', 'Naproxen'), ('meloxicam', 'Meloxicam'), ('celecoxib', 'Celecoxib')], default='allopurinol', max_length=60)),
                ('med_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='generic_name', unique=True, verbose_name='Medication Name')),
                ('dose', models.IntegerField(choices=[(50, '50 mg'), (100, '100 mg'), (150, '150 mg'), (200, '200 mg'), (250, '250 mg'), (300, '300 mg'), (350, '350 mg'), (400, '400 mg'), (450, '450 mg'), (500, '500 mg'), (550, '550 mg'), (600, '600 mg'), (650, '650 mg'), (700, '700 mg'), (750, '750 mg'), (800, '800 mg'), (850, '850 mg'), (900, '900 mg')])),
                ('side_effects', models.CharField(blank=True, choices=[('Rash', 'Rash'), ('Hypersensitivity syndrome', 'Hypersensitivity syndrome'), ('Elevated LFTs', 'Elevated LFTs'), ('Cytopenias', 'Cytopenias'), ('GI upset', 'GI upset')], help_text='Have you had any side effects?', max_length=100, null=True)),
                ('de_sensitized', models.BooleanField(blank=True, help_text='Have you been de-sensitized to allopurinol?', null=True)),
                ('drug_class', models.CharField(choices=[('urate-lowering therapy', 'Urate-lowering therapy'), ('systemic steroid', 'Systemic steroid'), ('anti-inflammatory', 'Anti-inflammatory'), ('nonsteroidal antiinflammatory drug', 'Nonsteroidal anti-inflammatory drug'), ('urate extreagogue', 'Urate excretagogue'), ('local steroid', 'Local steroid'), ('recombinant uricase', 'Recombinant uricase')], default='urate-lowering therapy', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
