# Generated by Django 3.1.4 on 2021-05-20 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210520_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='permission',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]