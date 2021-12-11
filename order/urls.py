from django.urls import path
from order.views import (
    OrderView,
    OrderInfoDetailView,
    PayInfoView,
)

urlpatterns = [
    path('', OrderView.as_view(), name = 'order_info'),
    path('<int:id>/', OrderInfoDetailView.as_view(), name = 'order_info_detail'),
    path('pay_info/', PayInfoView.as_view(), name = 'pay_info'),
]
