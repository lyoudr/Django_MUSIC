from django.db import transaction
from django.db.models import F
from django.db.models import Sum

from order.models import Order, OrderInfo, PayInfo
from order.serializers import (
    OrderSerializer, 
    OrderInfoSerializer,
    PayInfoSerializer,
)
from product.models import Product

from music.custom import CustomJsonResponse, CustomError
from music.pagination import CustomNumberPagination

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class OrderView(GenericAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomNumberPagination

    @swagger_auto_schema(
        operation_summary = 'order-01-get 取得使用者購物車的商品',
        manual_parameters = [
            openapi.Parameter(
                'page',
                in_ = openapi.IN_QUERY,
                description = 'page',
                type = openapi.TYPE_INTEGER,
                required = False
            ),
            openapi.Parameter(
                'page_size',
                in_ = openapi.IN_QUERY,
                description = 'page_size',
                type = openapi.TYPE_INTEGER,
                required = False
            )
        ]
    )
    def get(self, request):
        self.page = request.GET.get('page', None)
        self.page_size = request.GET.get('page_size', None)

        cond = {
            'status' : '01',
            'order_user': request.user,
        }
        orders = self.get_queryset().filter(**cond)
        if orders:
            if self.page:
                pg_data = self.paginate_queryset(orders)
                serializer = self.serializer_class(pg_data, many = True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.serializer_class(orders, many = True)
                data = serializer.data
            return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
        return CustomJsonResponse(result_data = [], status = status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_summary = 'order-02-post 新增商品至購物車',
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                'product_type_id': openapi.Schema(
                    type = openapi.TYPE_INTEGER,
                    description = '商品類別 KEY',
                    example = 1
                ),
                'product_id': openapi.Schema(
                    type = openapi.TYPE_INTEGER,
                    description = '商品 KEY',
                    example = 1
                ),
                'count': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '商品數量',
                    example = 3
                )
            }
        )
    )
    def post(self, request):
        with transaction.atomic():
            data = request.data

            ### 1. Count Price
            products = Product.objects.filter(pk = data.get('product_id'))
            if not products.count() == 1:
                raise CustomError(
                    return_code = 'product error',
                    status_code = status.HTTP_400_BAD_REQUEST,
                    return_message = 'can not find product'
                )
            price = products[0].price * data.get('count')

            ### 2. Update or Create Order
            # find if there were products in user's cart. 
            orders = Order.objects.filter(
                status = '01',
                order_user_id = request.user.pk,
                product_type＿id = data.get('product_type_id')
            )
            # If there were orders, merge orders. else create new order.
            if not orders.count() == 1:
                order_data = {
                    'status': '01',
                    'order_no': None,
                    'order_user': request.user,
                    'product_type_id': data.get('product_type_id'),
                    'total_price': price,
                }
                order = Order.objects.create(**order_data)
            # update orders total_price
            else:
                order = orders[0]
                order.total_price = order.total_price + price
                order.save()

            ### 2. OrderInfo
            data.update({
                'order_user_id': request.user.pk,
                'order_id': order.pk,
            })
            # If there were order_infos in the same order with same product_id, merge order_infos
            order_infos = OrderInfo.objects.filter(**{
                k:v for k, v in data.items() if k in ('order_id', 'order_user', 'product_id')
            })
            
            if order_infos.count() == 1:
                serializer = OrderInfoSerializer(
                    order_infos[0], 
                    data = {
                        'order_user_id': request.user.pk,
                        'order_id': order.pk,
                        'count': order_infos[0].count + data.get('count'),
                        'price': order_infos[0].price + price 
                    },
                    partial = True,
                )
            else:
                serializer = OrderInfoSerializer(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            # get user orders
            orders = self.queryset.filter(status = '01', order_user_id = request.user.pk)
            or_serializer = self.serializer_class(orders, many = True)
            data = or_serializer.data
        return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)

    
    @swagger_auto_schema(
        operation_summary = 'order-04-patch 確認下單',
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                'pay_info_id': openapi.Schema(
                    type = openapi.TYPE_INTEGER,
                    description = '付款 KEY',
                    example = 1
                ),
                'ship_addr': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '送貨地址',
                    example = '台北市大安區'
                )
            }
        )
    )
    def patch(self, request):
        data = request.data
        data['status'] = '02'
        print('data is =>', data)
        orders = self.queryset.filter(status = '01', order_user_id = request.user.pk)
        if orders:
            for order in orders:
                serializer = self.serializer_class(
                    order,
                    data = data,
                    partial = True
                )
                serializer.is_valid(raise_exception = True)
                serializer.save()
        else:
            raise CustomError(
                return_code = 'order-04-patch_update_error',
                return_message = f'no orders in cart',
                status_code = status.HTTP_404_NOT_FOUND,
            )
        or_serializer = self.serializer_class(orders, many = True)
        resp = or_serializer.data
        return CustomJsonResponse(result_data = resp, status = status.HTTP_200_OK)

    
class OrderInfoDetailView(GenericAPIView):
    model = OrderInfo
    queryset = model.objects.all()
    serializer_class = OrderInfoSerializer
    pagination_class = CustomNumberPagination

    @swagger_auto_schema(
        operation_summary = 'order-03-delete 從購物車移除商品'
    )
    def delete(self, request, id):
        self.page = request.GET.get('page', None)
        self.page_size = request.GET.get('page_size', None)
        # 1. check product id is in database
        with transaction.atomic():
            # delete
            try :
                order_info = self.queryset.get(pk = id)
                order = order_info.order
                order_info.delete()
                
                if order.order_info_a.count() == 0:
                    order.delete()
                else: # update order total_price
                    order.total_price = order.order_info_a.aggregate(Sum('price')).get('price__sum')
                    order.save()

            except OrderInfo.DoesNotExist:
                raise CustomError(
                    return_code = 'order-03-delete_not_found',
                    return_message = f'order_info_id {id} is not in cart',
                    status_code = status.HTTP_404_NOT_FOUND,
                )
        cond = {
            'status' : '01',
            'order_user': request.user,
        }
        orders = Order.objects.filter(**cond)
        if orders:
            if self.page:
                pg_data = self.paginate_queryset(orders)
                serializer = OrderSerializer(pg_data, many = True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = OrderSerializer(orders, many = True)
                data = serializer.data
            return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
        return CustomJsonResponse(result_data = [], status = status.HTTP_200_OK)
            
            


class PayInfoView(APIView):
    model = PayInfo
    queryset = model.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = PayInfoSerializer

    @swagger_auto_schema(
        operation_summary = 'pay-01-get 取得使用者付款資訊',
    )
    def get(self, request):
        pay_infos = self.queryset.filter(user_id = request.user.pk)
        serializer = self.serializer_class(pay_infos, many = True)
        data = serializer.data
        return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary = 'pay-02-post 創建付款資訊',
        manual_parameters = [
            openapi.Parameter(
                'bank',
                in_ = openapi.IN_QUERY,
                description = 'bank',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'card_no',
                in_ = openapi.IN_QUERY,
                description = 'card no',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'valid_no',
                in_ = openapi.IN_QUERY,
                description = 'card valid no',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'card_type',
                in_ = openapi.IN_QUERY,
                description = 'card type',
                type = openapi.TYPE_STRING,
                required = True
            ),
        ]
    )
    def post(self, request):
        data = {
            'bank': request.GET.get('bank'),
            'card_no': request.GET.get('card_no'),
            'valid_no': request.GET.get('valid_no'),
            'card_type': request.GET.get('card_type'),
            'user_id': request.user.pk
        }
        with transaction.atomic():
            serializer = self.serializer_class(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            resp = serializer.data
        return CustomJsonResponse(result_data = resp, status = status.HTTP_200_OK)


        








