# Generated by Django 3.1.4 on 2021-11-12 02:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20211013_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='updated_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]