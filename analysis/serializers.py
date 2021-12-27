from django_grpc_framework import proto_serializers

from rest_framework import serializers
from rest_framework import status

from analysis.grpc import sales_pb2

from product.models import ProductType
from music.utils.custom_exception import CustomError


class FeedBackSerializer(proto_serializers.ProtoSerializer):
    id = serializers.IntegerField()
    rank = serializers.CharField()
    user_id = serializers.IntegerField()
    product_type_id = serializers.IntegerField()
    description = serializers.CharField()
    product_type = serializers.SerializerMethodField()

    def get_product_type(self, data):
        try:
            product_type = ProductType.objects.get(pk = data.product_type_id)
        except ProductType.DoesNotExist:
            raise CustomError(
                return_message = 'can not find product type',
                return_code = 'can not find product type',
                status_code = status.HTTP_404_NOT_FOUND
            )
        return product_type.get_type_no_display()


    class Meta:
        proto_class = sales_pb2.FeedBack
        fields = ['id', 'rank', 'user_id', 'product_type_id', 'description', 'product_type']


class KeyWordSerializer(proto_serializers.ProtoSerializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    keyword = serializers.CharField()
    class Meta:
        proto_class = sales_pb2.KeyWord
        fields = ('id', 'user_id', 'keyword')