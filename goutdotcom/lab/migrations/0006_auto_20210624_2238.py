# Generated by Django 3.1.7 on 2021-06-24 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0005_auto_20210624_1939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alt',
            old_name='alt_sgpt',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='ast',
            old_name='ast_sgot',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='creatinine',
            old_name='creatinine',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='hemoglobin',
            old_name='hemoglobin',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='platelet',
            old_name='platelets',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='urate',
            old_name='uric_acid',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='wbc',
            old_name='white_blood_cells',
            new_name='value',
        ),
    ]
