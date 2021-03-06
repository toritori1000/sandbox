# Generated by Django 2.0.6 on 2018-09-07 22:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_eventdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventdate',
            old_name='centurie',
            new_name='century',
        ),
        migrations.RenameField(
            model_name='eventdate',
            old_name='date_in_mon',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='eventdate',
            old_name='end_centurie',
            new_name='end_century',
        ),
        migrations.AddField(
            model_name='eventdate',
            name='end_date',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(31), django.core.validators.MinValueValidator(1)]),
        ),
    ]
