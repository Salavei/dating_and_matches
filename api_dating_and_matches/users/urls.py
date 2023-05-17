from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import UserRegistrationAndRatingView, UserLoginView, UserUpdateAPIView

urlpatterns = [
    path('register/', UserRegistrationAndRatingView.as_view(), name='user-registration-and-rating'),
    path('users/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]