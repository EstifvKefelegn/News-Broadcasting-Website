# Generated by Django 5.0.1 on 2024-01-23 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0010_alter_news_promotion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion',
            name='description',
        ),
    ]
