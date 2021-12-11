from order.models import Order, OrderInfo, PayInfo

from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    product_type_name = serializers.SerializerMethodField()

    def get_product_type_name(self, instance):
        return instance.product_type.get_type_no_display()

    def to_representation(self, instance):
        orders = super(OrderSerializer, self).to_representation(instance)
        order_infos = instance.order_info_a.all()
        if order_infos:
            order_infos_serializer = OrderInfoSerializer(order_infos, many = True)
            order_infos = order_infos_serializer.data
            orders['order_infos'] = order_infos
        return orders
    class Meta:
        model = Order
        fields = ('id', 'order_no', 'status', 'order_user', 'product_type', 'product_type_name', 'total_price')

class OrderInfoSerializer(serializers.ModelSerializer):
    order_user_id = serializers.IntegerField()
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    count = serializers.IntegerField()
    price = serializers.IntegerField(required=False)
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
        fields = ('order_user_id', 'order_id', 'order_no', 'order_info_id', 'product_id', 'count', 'price', 'product_name', 'product_no', 'product_img',)


class ListOrderInfoSerializer(serializers.ListSerializer):
    child = OrderInfoSerializer()


class PayInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    bank = serializers.CharField(max_length = 4)
    valid_no = serializers.CharField(max_length = 4)
    card_type = serializers.CharField(max_length = 1)
    card_no = serializers.SerializerMethodField()
    bank_name = serializers.SerializerMethodField()
    card_name = serializers.SerializerMethodField()

    def get_card_no(self, instance):
        card_no = instance.card_no
        encrypted_card_no = card_no.replace(card_no[:11], '*'*12)
        return encrypted_card_no

    def get_bank_name(self, instance):
        return instance.get_bank_display()
    
    def get_card_name(self, instance):
        return instance.get_card_type_display()
    class Meta:
        model = PayInfo
        fields = ('id', 'user_id', 'bank', 'bank_name', 'card_no', 'valid_no', 'card_type', 'card_name')