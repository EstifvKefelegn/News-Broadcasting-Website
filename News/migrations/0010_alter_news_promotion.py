# Generated by Django 5.0.1 on 2024-01-23 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0009_news_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='promotion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='News.promotion'),
        ),
    ]