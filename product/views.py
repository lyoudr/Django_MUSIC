from django.db import transaction

from music.custom import CustomJsonResponse, CustomError
from music.pagination import CustomNumberPagination

from product.models import Product, ProductType
from product.serializers import ProductSerializer, ProductTypeSerializer

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductView(GenericAPIView):
    model = Product
    queryset = model.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomNumberPagination

    @swagger_auto_schema(
        operation_summary = 'get all user product',
        manual_parameters = [
            openapi.Parameter(
                'product_id',
                in_ = openapi.IN_QUERY,
                description = 'product id',
                type = openapi.TYPE_INTEGER,
                required = False,
            ),
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
            'owner': request.user,
            'pk': request.GET.get('product_id'),
        }
        products = self.queryset.filter(**{k:v for k, v in cond.items() if v})
        if products:
            if not request.GET.get('product_id'):
                if self.page:
                    pg_data = self.paginate_queryset(products)
                    serializer = self.serializer_class(pg_data, many = True)
                    data = self.get_paginated_response(serializer.data).data
                else:
                    serializer = self.serializer_class(products, many = True)
                    data = serializer.data
                return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
            if products.count() == 1:
                serializer = self.serializer_class(products[0])
                data = serializer.data
                return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
        return CustomJsonResponse(result_data = [], status = status.HTTP_200_OK)



    @swagger_auto_schema(
        operation_summary = 'create product',
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                'product_type_id': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '商品種類KEY',
                    example = 1,
                ),
                'product_name': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '商品名稱',
                    example = '譜名'
                ),
                'description': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '商品描述',
                    example = '商品描述'
                ),
                'owner_id' : openapi.Schema(
                   type = openapi.TYPE_INTEGER,
                   description = '商品所屬 user id',
                   example = 1 
                ),
                'blogpost_id': openapi.Schema(
                   type = openapi.TYPE_INTEGER,
                   description = 'blog 貼文 id',
                   example = 1 
                ),
                'price': openapi.Schema(
                   type = openapi.TYPE_INTEGER,
                   description = '商品價格',
                   example = 1 
                )
            }
        )
    )
    def post(self, request):
        data = request.data
        with transaction.atomic():
            prod_serializer = self.serializer_class(data = data)
            prod_serializer.is_valid(raise_exception = True)
            prod_serializer.save()
            data = prod_serializer.data
        return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_summary = 'update product',
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
                    example = 1,
                ),
                'product_name': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '商品名稱',
                    example = '譜名'
                ),
                'description': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '商品描述',
                    example = '商品描述'
                ),
                'owner_id' : openapi.Schema(
                type = openapi.TYPE_INTEGER,
                description = '商品所屬 user id',
                example = 1 
                ),
                'blogpost_id': openapi.Schema(
                type = openapi.TYPE_INTEGER,
                description = 'blog 貼文 id',
                example = 1 
                ),
                'price': openapi.Schema(
                type = openapi.TYPE_INTEGER,
                description = '商品價格',
                example = 1 
                )
            }
        )
    )
    def patch(self, request):
        data = request.data
        if not data.get('product_id'):
            raise CustomError(
                return_code = 'not fill required field : product_id',
                return_message = 'not fill required field : product_id',
                status_code = status.HTTP_404_NOT_FOUND
            )
        with transaction.atomic():
            try :
                product = self.queryset.get(pk = data.get('product_id'))
            except Product.DoesNotExist:
                raise CustomError(
                    return_code = 'can not find product',
                    return_message = 'can not find product',
                    status_code = status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(product, data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()

        return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
        

class ProductTypeView(APIView):
    model = ProductType
    queryset = model.objects.all()
    serializer_class = ProductTypeSerializer

    @swagger_auto_schema(
        operation_summary = 'get all product types'
    )
    def get(self, request):
        product_types = self.queryset.all()
        if product_types:
            serializer = self.serializer_class(product_types, many = True)
            data = serializer.data
            return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
        return CustomJsonResponse(result_data = [], status = status.HTTP_200_OK)


        
        