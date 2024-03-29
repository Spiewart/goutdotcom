# Generated by Django 3.1.7 on 2022-03-30 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ultplan', '0002_auto_20220313_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ultplan',
            options={},
        ),
        migrations.AddField(
            model_name='historicalultplan',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='Is this ULTPlan active?'),
        ),
        migrations.AddField(
            model_name='historicalultplan',
            name='emergency',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Has this ULTPLan been paused for an emergency?'),
        ),
        migrations.AddField(
            model_name='historicalultplan',
            name='inactive',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this ULTPlan inactive?'),
        ),
        migrations.AddField(
            model_name='ultplan',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='Is this ULTPlan active?'),
        ),
        migrations.AddField(
            model_name='ultplan',
            name='emergency',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Has this ULTPLan been paused for an emergency?'),
        ),
        migrations.AddField(
            model_name='ultplan',
            name='inactive',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Is this ULTPlan inactive?'),
        ),
        migrations.AlterField(
            model_name='ultplan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='ultplan',
            constraint=models.UniqueConstraint(condition=models.Q(active=True), fields=('user',), name='user_active_ultplan'),
        ),
    ]
