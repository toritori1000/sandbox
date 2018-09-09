# Generated by Django 2.0.6 on 2018-09-09 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_eventdate_decade_by_five'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='event_date',
            field=models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_date_set', to='blog.EventDate'),
        ),
    ]