from django.db import transaction

from music.custom import CustomJsonResponse, CustomError
from music.pagination import CustomNumberPagination

from product.models import Product
from product.serializers import ProductSerializer

from rest_framework.generics import GenericAPIView
from rest_framework import serializers, status

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

        products = self.get_queryset()
        if products:
            if self.page:
                pg_data = self.paginate_queryset(products)
                serializer = self.serializer_class(pg_data, many = True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.serializer_class(products, many = True)
                data = serializer.data
            return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
        return CustomJsonResponse(result_data = [], status = status.HTTP_200_OK)



    @swagger_auto_schema(
        operation_summary = 'create product',
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
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
            type = openapi.TYPE_ARRAY,
            items = openapi.Items(
                type = openapi.TYPE_OBJECT,
                properties = {
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
    )
    def patch(self, request):
        re_ids = [product.get('product_id') for product in request.data] # update product id
        with transaction.atomic():
            serializer = self.serializer_class(data = request.data[0])
            
            for db_product in self.get_queryset():
                if db_product.pk not in re_ids:
                    db_product.delete()
            
            for product in request.data:
                pro_id = product.get('product_id')
                
                if pro_id:
                    try :
                        db_product = self.get_queryset().get(pk = pro_id)
                    except Product.DoesNotExist:
                        raise CustomError(
                            return_code = '01XX',
                            return_message = 'product is not in database',
                            status_code = status.HTTP_400_BAD_REQUEST,
                        )
                    serializer = self.serializer_class(
                        db_product,
                        data = product,
                        partial = False,
                    )
                else:
                    serializer = self.serializer_class(data = product)

                serializer.is_valid(raise_exception = True)
                serializer.save()
            
            
            data = self.serializer_class(self.get_queryset(), many = True).data

            return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)
        




        
        