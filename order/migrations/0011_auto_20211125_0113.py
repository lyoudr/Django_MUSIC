# Generated by Django 3.1.4 on 2021-11-25 01:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_payinfo_valid_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='payinfo',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payinfo',
            name='updated_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='payinfo',
            name='valid_no',
            field=models.CharField(default=123, max_length=4),
            preserve_default=False,
        ),
    ]