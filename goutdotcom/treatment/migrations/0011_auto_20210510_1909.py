# Generated by Django 3.1.7 on 2021-05-10 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0010_auto_20210430_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allopurinol',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='celecoxib',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='colchicine',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='febuxostat',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='ibuprofen',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='meloxicam',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='methylprednisolone',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='naproxen',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='prednisone',
            name='med_slug',
        ),
        migrations.RemoveField(
            model_name='probenecid',
            name='med_slug',
        ),
        migrations.AddField(
            model_name='celecoxib',
            name='as_prophylaxis',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this for flare prophylaxis while initiating ULT?', verbose_name='Flare prophylaxis?'),
        ),
        migrations.AddField(
            model_name='colchicine',
            name='as_prophylaxis',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this for flare prophylaxis while initiating ULT?', verbose_name='Flare prophylaxis?'),
        ),
        migrations.AddField(
            model_name='ibuprofen',
            name='as_prophylaxis',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this for flare prophylaxis while initiating ULT?', verbose_name='Flare prophylaxis?'),
        ),
        migrations.AddField(
            model_name='meloxicam',
            name='as_prophylaxis',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this for flare prophylaxis while initiating ULT?', verbose_name='Flare prophylaxis?'),
        ),
        migrations.AddField(
            model_name='methylprednisolone',
            name='as_injection',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Was this given by an injection into your joint?', verbose_name='Given by joint injection?'),
        ),
        migrations.AddField(
            model_name='naproxen',
            name='as_prophylaxis',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this for flare prophylaxis while initiating ULT?', verbose_name='Flare prophylaxis?'),
        ),
        migrations.AddField(
            model_name='prednisone',
            name='as_prophylaxis',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this for flare prophylaxis while initiating ULT?', verbose_name='Flare prophylaxis?'),
        ),
    ]
