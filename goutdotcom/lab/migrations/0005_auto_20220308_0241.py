# Generated by Django 3.1.7 on 2022-03-08 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_auto_20220308_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baselinealt',
            name='value',
            field=models.IntegerField(default=35, help_text='ALT (SGPT) is typically reported in units per liter (U/L)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='baselineast',
            name='value',
            field=models.IntegerField(default=35, help_text='AST (SGOT) is typically reported in units per liter (U/L)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='baselinehemoglobin',
            name='value',
            field=models.DecimalField(decimal_places=1, default=14.0, help_text='HGB (hemoglobin) is typically reporeted in grams per deciliter (g/dL)', max_digits=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='baselineplatelet',
            name='value',
            field=models.IntegerField(default=333, help_text='PLT (platelets) is typically reported in platelets per microliter (PLT/microL)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='baselinewbc',
            name='value',
            field=models.DecimalField(decimal_places=1, default=14.0, help_text='WBC (white blood cells) is typically reported as cells per cubic millimeter (cells/mm^3)', max_digits=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalbaselinealt',
            name='value',
            field=models.IntegerField(default=35, help_text='ALT (SGPT) is typically reported in units per liter (U/L)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalbaselineast',
            name='value',
            field=models.IntegerField(default=35, help_text='AST (SGOT) is typically reported in units per liter (U/L)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalbaselinehemoglobin',
            name='value',
            field=models.DecimalField(decimal_places=1, default=14.0, help_text='HGB (hemoglobin) is typically reporeted in grams per deciliter (g/dL)', max_digits=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalbaselineplatelet',
            name='value',
            field=models.IntegerField(default=333, help_text='PLT (platelets) is typically reported in platelets per microliter (PLT/microL)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalbaselinewbc',
            name='value',
            field=models.DecimalField(decimal_places=1, default=14.0, help_text='WBC (white blood cells) is typically reported as cells per cubic millimeter (cells/mm^3)', max_digits=3),
            preserve_default=False,
        ),
    ]
