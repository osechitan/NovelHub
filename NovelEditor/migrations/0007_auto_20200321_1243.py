# Generated by Django 3.0.4 on 2020-03-21 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NovelEditor', '0006_novelhistory_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='max_revision_id',
            field=models.IntegerField(null=True, verbose_name='更新バージョン'),
        ),
        migrations.AddField(
            model_name='novel',
            name='revision_id',
            field=models.IntegerField(null=True, verbose_name='更新バージョン'),
        ),
        migrations.AddField(
            model_name='novelhistory',
            name='revision_id',
            field=models.IntegerField(null=True, verbose_name='更新バージョン'),
        ),
        migrations.AlterField(
            model_name='novelhistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日'),
        ),
    ]
