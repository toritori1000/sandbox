# Generated by Django 2.0.6 on 2018-09-03 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimage',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to='images/blog'),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img3_created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img3_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img3_external_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img3_title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img4',
            field=models.ImageField(blank=True, null=True, upload_to='images/blog'),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img4_created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img4_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img4_external_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postimage',
            name='img4_title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='images/blog'),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='img2_created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='img2_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='img2_external_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='img2_title',
            field=models.TextField(blank=True, null=True),
        ),
    ]