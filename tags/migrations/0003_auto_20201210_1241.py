# Generated by Django 3.1.4 on 2020-12-10 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0002_hierarchicaltag_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hierarchicaltag',
            name='user',
        ),
        migrations.AddField(
            model_name='contentitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
