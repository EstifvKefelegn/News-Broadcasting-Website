# Generated by Django 5.0.1 on 2024-01-27 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0015_alter_review_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='promotion',
        ),
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
        migrations.AddField(
            model_name='promotion',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='News.news'),
        ),
    ]