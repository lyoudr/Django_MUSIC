from django.urls import path
from product.views import (
    ProductView,
    ProductTypeView,
)

urlpatterns = [
    path('', ProductView.as_view(), name = 'product'),
    path('type', ProductTypeView.as_view(), name = 'product_type'),
]
