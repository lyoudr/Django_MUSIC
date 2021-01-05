from django.urls import path
from login.views import (
    LogInView
)

urlpatterns = [
    path('login/', LogInView.as_view())
]