# Generated by Django 3.0.4 on 2020-03-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NovelEditor', '0008_auto_20200322_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novelhistory',
            name='revision_id',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='バージョン'),
        ),
    ]
