from music.custom import CustomJsonResponse, CustomError
from analysis.grpc.client import get_analysis

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
        resp = get_analysis()
        return CustomJsonResponse(result_data = resp, status = status.HTTP_200_OK)


        

