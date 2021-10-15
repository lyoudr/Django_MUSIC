from django.urls import path
from order.views import (
    OrderInfoView,
    OrderInfoDetailView,
)

urlpatterns = [
    path('', OrderInfoView.as_view(), name = 'order_info'),
    path('<int:id>/', OrderInfoDetailView.as_view(), name = 'order_info_detail')
]
