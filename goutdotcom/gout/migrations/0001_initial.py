# Generated by Django 3.0.3 on 2020-04-23 21:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('first_name', models.CharField(help_text='Enter first name', max_length=128)),
                ('last_name', models.CharField(help_text='Enter last name', max_length=128)),
                ('age', models.IntegerField(help_text='Enter age', verbose_name=range(0, -149))),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], help_text='Enter gender', max_length=6)),
                ('mrn', models.IntegerField(help_text='Enter MRN', primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urate', models.FloatField()),
                ('creatinine', models.FloatField()),
                ('BMI', models.IntegerField()),
                ('drinks_per_week', models.IntegerField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gout.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Flare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('location', models.CharField(choices=[('Toe', 'Toe'), ('Ankle', 'Ankle'), ('Knee', 'Knee'), ('Hip', 'Hip'), ('Finger', 'Finger'), ('Wrist', 'Wrist'), ('Elbow', 'Elbow'), ('Shoulder', 'Shoulder')], default='Toe', help_text='What joint did the flare occur in?', max_length=8)),
                ('treated_with', models.CharField(choices=[('NSAID', 'NSAID'), ('colchicine', 'colchicine'), ('PO steroid', 'PO steroid'), ('INJ steroid', 'INJ steroid'), ('Tincture of time', 'Tincture of time')], default='NSAID', help_text='What was the flare treated with?', max_length=20)),
                ('duration', models.IntegerField(help_text='How long did it last? (days)')),
                ('urate_at_flare', models.DecimalField(decimal_places=1, help_text='What was the uric acid at the time of the flare?', max_digits=3)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gout.Patient')),
            ],
            options={
                'ordering': ['patient'],
            },
        ),
    ]
