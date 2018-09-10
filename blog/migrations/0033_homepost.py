# Generated by Django 2.0.6 on 2018-09-10 00:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_auto_20180910_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('caption', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('alt_text', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('posts', models.ManyToManyField(default=1, related_name='home_posts', to='blog.Post')),
            ],
            options={
                'verbose_name_plural': 'HomePosts',
                'ordering': ['created_date'],
                'verbose_name': 'HomePost',
            },
        ),
    ]
