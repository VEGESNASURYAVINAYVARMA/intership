from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterView, RequestPasswordResetView, UserLoginView, VerifyOTPView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request_password_reset'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
