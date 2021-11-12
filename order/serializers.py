from order.models import Order, OrderInfo

from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderInfoSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    count = serializers.IntegerField()
    price = serializers.IntegerField(read_only = True)
    order_no = serializers.SerializerMethodField()
    order_info_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_no = serializers.SerializerMethodField()
    product_img = serializers.SerializerMethodField()

    def get_order_no(self, instance):
        return instance.order.order_no

    def get_order_info_id(self, instance):
        return instance.pk

    def get_product_name(self, instance):
        return instance.product.product_name

    def get_product_no(self, instance):
        return instance.product.product_no
    
    def get_product_img(self, instance):
        return instance.product.blogpost.photo.url

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'order_no', 'order_info_id', 'product_id', 'count', 'price', 'product_name', 'product_no', 'product_img',)


class ListOrderInfoSerializer(serializers.ListSerializer):
    child = OrderInfoSerializer()

