# Generated by Django 3.1.7 on 2021-11-10 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_auto_20211111_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bleed',
            name='GIB',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Have you ever had <a href='https://en.wikipedia.org/wiki/Gastrointestinal_bleeding' target='_blank'>gastrointestinal bleeding</a>?", null=True),
        ),
        migrations.AlterField(
            model_name='chf',
            name='systolic',
            field=models.BooleanField(blank=True, choices=[(True, 'Systolic'), (False, 'Diastolic')], help_text="Do you have systolic (reduced <a href='https://en.wikipedia.org/wiki/Ejection_fraction' target='_blank'>ejection fraction</a>) heart failure?", null=True, verbose_name='Systolic or diastolic heart failure'),
        ),
        migrations.AlterField(
            model_name='chf',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Do you have CHF (<a href='https://en.wikipedia.org/wiki/Heart_failure' target='_blank'>congestive heart failure</a>)?", null=True, verbose_name='Congestive Heart Failure (CHF)'),
        ),
        migrations.AlterField(
            model_name='ckd',
            name='dialysis',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], help_text="Are you on <a href='https://en.wikipedia.org/wiki/Hemodialysis' target='_blank'>dialysis</a>?", null=True),
        ),
        migrations.AlterField(
            model_name='ckd',
            name='stage',
            field=models.IntegerField(choices=[(1, 'I'), (2, 'Ii'), (3, 'Iii'), (4, 'Iv'), (5, 'V')], default=None, help_text="What <a href='https://www.kidney.org/sites/default/files/01-10-7278_HBG_CKD_Stages_Flyer_GFR.gif' target='_blank'>stage</a> is your CKD??", null=True, verbose_name='CKD stage'),
        ),
        migrations.AlterField(
            model_name='ckd',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Do you have CKD (<a href='https://en.wikipedia.org/wiki/Chronic_kidney_disease' target='_blank'>chronic kidney disease</a>)?", null=True, verbose_name='Chronic Kidney Disease (CKD)'),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='insulin',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Are you on <a href='https://en.wikipedia.org/wiki/Insulin' target='_blank'>kidney stones</a>?", null=True),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='type',
            field=models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two')], help_text="Do you have <a href='https://en.wikipedia.org/wiki/Type_1_diabetes' target='_blank'>type I</a> or <a href='https://en.wikipedia.org/wiki/Type_2_diabetes' target='_blank'>type II</a> diabetes?", null=True, verbose_name='Type 1 or type 2 diabetes?'),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Do you have <a href='https://en.wikipedia.org/wiki/Diabetes' target='_blank'>diabetes</a>?", null=True, verbose_name='Diabetes'),
        ),
        migrations.AlterField(
            model_name='heartattack',
            name='cabg',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Have you had <a href='https://en.wikipedia.org/wiki/Coronary_artery_bypass_surgery' target='_blank'>bypass</a>?", null=True, verbose_name='cabg'),
        ),
        migrations.AlterField(
            model_name='heartattack',
            name='stent',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Have you had one or more <a href='https://en.wikipedia.org/wiki/Stent' target='_blank'>stent</a> placed?", null=True, verbose_name='stent'),
        ),
        migrations.AlterField(
            model_name='heartattack',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Have you ever had <a href='https://en.wikipedia.org/wiki/Myocardial_infarction' target='_blank'>heart attack</a>?", null=True, verbose_name='heart attack'),
        ),
        migrations.AlterField(
            model_name='hypertension',
            name='medication',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Are you on <a href='https://www.heart.org/en/health-topics/high-blood-pressure/changes-you-can-make-to-manage-high-blood-pressure/types-of-blood-pressure-medications' target='_blank'>medications</a> for high blood pressure?", null=True, verbose_name='Blood pressure medications'),
        ),
        migrations.AlterField(
            model_name='ibd',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Do you have <a href='https://en.wikipedia.org/wiki/Inflammatory_bowel_disease' target='_blank'>IBD</a> (inflammatory bowel disease=Crohn's disease or ulcerative colitis)?", null=True, verbose_name='Inflammatory Bowel Disease'),
        ),
        migrations.AlterField(
            model_name='osteoporosis',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Do you have <a href='https://en.wikipedia.org/wiki/Osteoporosis' target='_blank'>osteoporosis</a>?", null=True, verbose_name='Osteoporosis'),
        ),
        migrations.AlterField(
            model_name='stroke',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Have you ever had <a href='https://en.wikipedia.org/wiki/Stroke' target='_blank'>stroke</a>?", null=True, verbose_name='stroke'),
        ),
        migrations.AlterField(
            model_name='uratekidneystones',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Have you had urate <a href='https://en.wikipedia.org/wiki/Kidney_stone_disease' target='_blank'>kidney stones</a>?", null=True, verbose_name='Urate Kidney Stones'),
        ),
        migrations.AlterField(
            model_name='xoiinteractions',
            name='value',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Are you on <a href='https://en.wikipedia.org/wiki/Mercaptopurine' target='_blank'>mercaptopurine</a> (6-MP, Purixan), <a href='https://en.wikipedia.org/wiki/Azathioprine' target='_blank'>azathioprine</a> (AZA, Imuran)?", null=True),
        ),
    ]
