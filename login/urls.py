from django.urls import path
from login.views import (
    RegisterView,
    LogInView,
    LogOutView,
    ForgetPassWordView,
    ResetPassWordView
)

urlpatterns = [
    path('user/register/', RegisterView.as_view()),
    path('user/login/', LogInView.as_view()),
    path('user/logout/', LogOutView.as_view()),
    path('password/forget_password/', ForgetPassWordView.as_view()),
    path('password/reset_password/', ResetPassWordView.as_view())
]