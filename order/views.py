from django.db import transaction

from order.models import Order, OrderInfo
from order.serializers import OrderSerializer, OrderInfoSerializer, ListOrderInfoSerializer

from music.custom import CustomJsonResponse, CustomError
from music.pagination import CustomNumberPagination

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import serializers, status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class OrderInfoView(GenericAPIView):
    model = OrderInfo
    queryset = model.objects.all()
    serializer_class = OrderInfoSerializer
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
            'order__isnull': True,
            'order_user_id': request.user.pk,
        }
        order_infos = self.get_queryset().filter(**cond)
        if order_infos:
            if self.page:
                pg_data = self.paginate_queryset(order_infos)
                serializer = self.serializer_class(pg_data, many = True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.serializer_class(order_infos, many = True)
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
            data.update({'order_user': request.user})
            
            ### 1. Order
            # find if there were products in user's cart. 
            orders = Order.objects.filter(
                status = '01',
                order_user_id = request.user.pk,
                product_type＿id = data.get('product_type_id')
            )
            # If there were, merge orders. else create new order.
            if not orders.count() == 1:
                order_data = {
                    'status': '01',
                    'order_no': None,
                    'order_user': request.user,
                    'product_type_id': data.get('product_type_id')
                }
                order = Order.objects.create(**order_data)
                
            ### 2. OrderInfo
            data.update({
                'order_id': orders[0].pk if orders.count() == 1 else order.pk
            })
            serializer = self.serializer_class(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
        return CustomJsonResponse(result_data = serializer.data, status = status.HTTP_200_OK)


class OrderInfoDetailView(GenericAPIView):
    model = OrderInfo
    queryset = model.objects.all()
    serializer_class = OrderInfoSerializer

    @swagger_auto_schema(
        operation_summary = 'order-03-delete 從購物車移除商品'
    )
    def delete(self, request, id):
        # 1. check product id is in database
        cond = {
            'order__isnull': True,
            'order_user_id': request.user.pk,
        }

        order_infos = self.get_queryset().filter(**cond)
        if order_infos:
            with transaction.atomic():
                # delete
                try :
                    order_info = order_infos.get(pk = id)
                    order_info.delete()
                except OrderInfo.DoesNotExist:
                    raise CustomError(
                        return_code = 'order-03-delete_not_found',
                        return_message = f'order_info_id {id} is not in cart',
                        status_code = status.HTTP_404_NOT_FOUND,
                    )
                # return remaining orders
                order_infos = self.get_queryset().filter(**cond)
                serializer = self.serializer_class(order_infos, many = True)
                resp = serializer.data
                return CustomJsonResponse(result_data = resp, status = status.HTTP_200_OK)
        return CustomJsonResponse(result_data = [], status = status.HTTP_200_OK)
            
            
            

        








