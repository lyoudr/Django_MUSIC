# Generated by Django 3.1.4 on 2021-03-04 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='role_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.CharField(choices=[(1, 'admin'), (2, 'manager'), (3, 'normal_member'), (4, 'vip_member')], max_length=255),
        ),
    ]
