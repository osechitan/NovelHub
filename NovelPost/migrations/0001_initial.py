# Generated by Django 3.0.4 on 2020-06-19 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NovelPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('body', models.TextField(null=True, verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'db_table': 'novel_post',
            },
        ),
    ]