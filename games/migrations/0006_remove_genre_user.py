# Generated by Django 4.2.4 on 2024-03-12 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_genre_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='user',
        ),
    ]
