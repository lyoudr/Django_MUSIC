from product.models import Product

from rest_framework import serializers
from rest_framework import status

class ProductSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField()
    blogpost_id = serializers.IntegerField()

    def get_product_id(self, instance):
        return instance.pk

    def create(self, data):
        print('data is =>', data)
        new_product = Product.objects.create(**data)
        return new_product

    class Meta:
        model = Product
        fields = (
            'product_id',
            'owner_id',
            'product_name',
            'description',
            'product_no',
            'blogpost_id',
            'price',
        )