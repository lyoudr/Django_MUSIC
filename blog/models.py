from django.db import models
from django.contrib.auth.models import User
from music.storage import select_storage

import django.utils.timezone as timezone


class BlogClass(models.Model):
    name = models.CharField(max_length = 255, unique = True)

    def __str__(self):
        return self.name



class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 2)
    blogclass = models.ForeignKey(BlogClass, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    photo = models.FileField(upload_to = 'blog_photos', storage = select_storage)
    music_sheet = models.FileField(upload_to = 'blog_sheets', storage = select_storage)
    description = models.CharField(max_length = 255)
    created_time = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title



class BlogSection(models.Model):
    blogpost = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
    order = models.IntegerField()
    post_type = models.CharField(max_length = 255, choices = (
        ('T', 'text'),
        ('P', 'photo'),
        ('V', 'video')
    ))
    text = models.TextField(null = True)
    photo = models.FileField(upload_to = 'blog_photos', storage = select_storage)
    video = models.CharField(max_length = 255, null = True)

    def __str__(self):
        return f'{self.blogpost.title}-{self.order}'