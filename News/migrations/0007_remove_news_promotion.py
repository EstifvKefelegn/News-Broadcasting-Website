# Generated by Django 5.0.1 on 2024-01-21 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0006_news_small_image_news_small_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='promotion',
        ),
    ]