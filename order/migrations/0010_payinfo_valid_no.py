# Generated by Django 3.1.4 on 2021-11-25 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20211125_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='payinfo',
            name='valid_no',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
