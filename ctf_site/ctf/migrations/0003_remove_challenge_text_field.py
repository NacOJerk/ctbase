# Generated by Django 3.0.6 on 2020-06-13 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctf', '0002_category_challenge_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='text_field',
        ),
    ]