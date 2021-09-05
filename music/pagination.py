from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomNumberPagination(PageNumberPagination):
    page = 1
    page_size = 12
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', None)),
            'page_size': int(self.request.GET.get('page_size', None)),
            'data': data
        })
