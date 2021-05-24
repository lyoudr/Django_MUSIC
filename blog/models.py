from django.db import models
from django.contrib.auth.models import User
from music.storage import select_storage

import django.utils.timezone as timezone


class BlogClass(models.Model):
    name = models.CharField(max_length = 255, unique = True)

    def __str__(self):
        return self.name

class BlogPhoto(models.Model):
    image = models.FileField(upload_to = 'blog_photos', storage = select_storage)

    def __str__(self):
        return self.image.name

    def delete(self):
        self.image.delete(save = True)
        super(BlogPhoto, self).delete()
    

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 2)
    blogclass = models.ForeignKey(BlogClass, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    photo = models.FileField(upload_to = 'blog_photos', storage = select_storage)
    music_sheet = models.FileField(upload_to = 'blog_sheets', storage = select_storage)
    description = models.CharField(max_length = 255)
    permission = models.IntegerField(default = 2) # private : 1, public : 2
    created_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

    def delete(self):
        self.photo.delete(save = True)
        self.music_sheet.delete(save = True)
        super(BlogPost, self).delete()


class BlogSection(models.Model):
    blogpost = models.ForeignKey(BlogPost, on_delete = models.CASCADE, related_name = 'blog_section')
    order = models.IntegerField()
    post_type = models.CharField(max_length = 255, choices = (
        ('T', 'text'),
        ('P', 'photo'),
        ('V', 'video')
    ))
    text = models.TextField(null = True)
    photo = models.ForeignKey(BlogPhoto, on_delete = models.CASCADE, related_name = 'blog_section', null = True)
    video = models.CharField(max_length = 255, null = True)

    def __str__(self):
        return f'{self.blogpost.title}-{self.order}'