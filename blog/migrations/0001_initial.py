# Generated by Django 3.1.4 on 2020-12-22 08:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import music.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('photo', models.FileField(storage=music.storage.select_storage, upload_to='blog_photos')),
                ('music_sheet', models.FileField(storage=music.storage.select_storage, upload_to='blog_sheets')),
                ('description', models.CharField(max_length=255)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('blogclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogclass')),
            ],
        ),
        migrations.CreateModel(
            name='BlogSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('post_type', models.CharField(choices=[('T', 'text'), ('P', 'photo'), ('V', 'video')], max_length=255)),
                ('text', models.TextField(null=True)),
                ('photo', models.FileField(storage=music.storage.select_storage, upload_to='blog_photos')),
                ('video', models.CharField(max_length=255, null=True)),
                ('blogpost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost')),
            ],
        ),
    ]
