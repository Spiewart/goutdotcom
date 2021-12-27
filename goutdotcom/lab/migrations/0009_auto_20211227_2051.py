# Generated by Django 3.1.7 on 2021-12-27 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0008_auto_20211225_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alt',
            name='date_drawn',
            field=models.DateField(blank=True, default=None, help_text='What day was this lab drawn?', null=True),
        ),
        migrations.AlterField(
            model_name='ast',
            name='date_drawn',
            field=models.DateField(blank=True, default=None, help_text='What day was this lab drawn?', null=True),
        ),
        migrations.AlterField(
            model_name='creatinine',
            name='date_drawn',
            field=models.DateField(blank=True, default=None, help_text='What day was this lab drawn?', null=True),
        ),
        migrations.AlterField(
            model_name='hemoglobin',
            name='date_drawn',
            field=models.DateField(blank=True, default=None, help_text='What day was this lab drawn?', null=True),
        ),
        migrations.AlterField(
            model_name='platelet',
            name='date_drawn',
            field=models.DateField(blank=True, default=None, help_text='What day was this lab drawn?', null=True),
        ),
        migrations.AlterField(
            model_name='urate',
            name='date_drawn',
            field=models.DateField(blank=True, default=None, help_text='What day was this lab drawn?', null=True),
        ),
        migrations.AlterField(
            model_name='wbc',
            name='date_drawn',
            field=models.DateField(blank=True, default=None, help_text='What day was this lab drawn?', null=True),
        ),
    ]
