# Generated by Django 3.1.7 on 2021-11-20 23:04

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_auto_20211115_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organtransplant',
            name='organ',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Heart', 'Heart'), ('Kidney', 'Kidney'), ('Liver', 'Liver'), ('Lung', 'Lung'), ('Pancreas', 'Pancreas'), ('Face', 'Face')], default='', help_text='Which organ did you have transplanted?', max_length=37, null=True, verbose_name='Organ(s) transplanted'),
        ),
    ]
