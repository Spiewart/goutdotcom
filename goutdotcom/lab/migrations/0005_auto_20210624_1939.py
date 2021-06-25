# Generated by Django 3.1.7 on 2021-06-24 19:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_auto_20210531_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='alt',
            name='date_drawn',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='What day was this lab drawn?'),
        ),
        migrations.AddField(
            model_name='ast',
            name='date_drawn',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='What day was this lab drawn?'),
        ),
        migrations.AddField(
            model_name='creatinine',
            name='date_drawn',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='What day was this lab drawn?'),
        ),
        migrations.AddField(
            model_name='hemoglobin',
            name='date_drawn',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='What day was this lab drawn?'),
        ),
        migrations.AddField(
            model_name='platelet',
            name='date_drawn',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='What day was this lab drawn?'),
        ),
        migrations.AddField(
            model_name='urate',
            name='date_drawn',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='What day was this lab drawn?'),
        ),
        migrations.AddField(
            model_name='wbc',
            name='date_drawn',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='What day was this lab drawn?'),
        ),
    ]
