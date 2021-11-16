from product.models import Product, ProductType

from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField()
    blogpost_id = serializers.IntegerField()
    product_type_id = serializers.IntegerField()
    product_name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    product_id = serializers.SerializerMethodField()
    product_img = serializers.SerializerMethodField()

    def get_product_id(self, instance):
        return instance.pk

    def get_product_img(self, instance):
        return instance.blogpost.photo.url

    class Meta:
        model = Product
        fields = (
            'product_type_id',
            'product_id',
            'owner_id',
            'product_name',
            'description',
            'product_no',
            'blogpost_id',
            'price',
            'product_img',
        )

class ProductTypeSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField()

    def get_type_name(self, instance):
        return instance.get_type_no_display()
    class Meta:
        model = ProductType
        fields = ('id', 'type_no', 'type_name')