import uuid
from django.db import models
from django.contrib.auth.models import User

from blog.models import BlogPost

class ProductType(models.Model):
    class Meta:
        db_table = 'PRODUCT_TYPE'
    
    TYPE_CHOICES = (
        ('PS', 'piano_sheet'),
        ('BK', 'book'),
        ('CL', 'clothes'),
    )

    type_no = models.CharField(max_length = 2, choices = TYPE_CHOICES)
    
    def __str__(self):
        return f'{self.type_no}'


class Product(models.Model):
    class Meta:
        db_table = 'PRODUCT'
    
    product_type = models.ForeignKey(ProductType, on_delete = models.CASCADE, related_name = 'product_c')
    product_no = models.UUIDField(default = uuid.uuid4, editable = True)
    product_name = models.CharField(max_length = 40)
    description = models.CharField(max_length = 200)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'product_a')
    blogpost = models.ForeignKey(BlogPost, on_delete = models.CASCADE, related_name = 'product_b')
    price = models.IntegerField()

    def __str__(self):
        return self.product_no
