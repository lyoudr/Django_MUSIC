from django.core import serializers
from music.custom import CustomJsonResponse
from analysis.grpc.client import GrpcClient
from analysis.serializers import FeedBackSerializer

from rest_framework.views import APIView
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AnalysisView(APIView):


    @swagger_auto_schema(
        operation_summary = 'analysis-01-get 取得銷售統計資料',
    )
    def get(self, request):
        """
        Return a list of sales report.
        """
        grpc_cl = GrpcClient()
        resp = grpc_cl.get_analysis()
        return CustomJsonResponse(result_data = resp, status = status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_summary = 'analysis-02-post 創建回饋資料',
        request_body = openapi.Schema( 
            type = openapi.TYPE_OBJECT,
            properties = {
                'rank': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '排名',
                    example = 1
                ),
                'product_type_id': openapi.Schema(
                    type = openapi.TYPE_INTEGER,
                    description = '商品類別 KEY',
                    example = 1
                ),
                'description': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = '使用感受',
                    example = 'good'
                )
            }
        )
    )
    def post(self, request):
        datas = request.data
        grpc_cl = GrpcClient()
        resp = grpc_cl.post_feedback(datas, request.user.pk)
        serializer = FeedBackSerializer(resp)
        data = serializer.data
        return CustomJsonResponse(result_data = data, status = status.HTTP_200_OK)




        

