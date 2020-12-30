from django.urls import path
from login.views import (
    log_in
)

urlpatterns = [
    path('login/', log_in)
]