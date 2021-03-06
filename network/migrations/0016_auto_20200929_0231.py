# Generated by Django 3.0.8 on 2020-09-29 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_auto_20200924_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='by_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
