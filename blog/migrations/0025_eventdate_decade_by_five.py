# Generated by Django 2.0.6 on 2018-09-08 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20180908_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdate',
            name='decade_by_five',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]