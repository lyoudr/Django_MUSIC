# Generated by Django 3.1.4 on 2021-10-05 02:06

from django.db import migrations, models
import music.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SysPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(storage=music.storage.select_storage, upload_to='sys_photos')),
            ],
            options={
                'db_table': 'SYS_PHOTO',
            },
        ),
        migrations.CreateModel(
            name='SysSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheet', models.FileField(storage=music.storage.select_storage, upload_to='sys_sheets')),
            ],
            options={
                'db_table': 'SYS_SHEET',
            },
        ),
    ]
