# Generated by Django 3.1.4 on 2020-12-10 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_user_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tags',
        ),
    ]
