# Generated by Django 3.1.7 on 2022-02-03 06:37

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
            name='ULT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('num_flares', models.CharField(blank=True, choices=[('zero', 'Zero'), ('one', 'One'), ('1-3', '2-3'), ('4-6', '4-6'), ('7 or more', '7 or more')], default='', help_text='If more than one, an estimate is fine!', max_length=30, null=True, verbose_name='How many gout flares have you had?')),
                ('freq_flares', models.CharField(blank=True, choices=[('one', 'One'), ('two or more', 'Two or more')], default='one', help_text='An estimate is fine!', max_length=30, null=True, verbose_name='Approximately how many flares do you have per year?')),
                ('ckd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.ckd')),
                ('erosions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.erosions')),
                ('hyperuricemia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.hyperuricemia')),
                ('stones', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.uratekidneystones')),
                ('tophi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='history.tophi')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
