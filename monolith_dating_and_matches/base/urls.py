from django.contrib.auth.views import LogoutView
from django.urls import path
from base import views

urlpatterns = [
    path('', views.StartPageView.as_view(), name='start_page'),
    path('register/', views.register_page, name='registry_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path('match/', views.MathPageView.as_view(), name='home_page'),
    path('login/', views.LoginPageView.as_view(), name='login_page'),
    path('chat/<str:hash>/', views.chat_page, name='chat_page'),
    path('profile/', views.user_profile, name='user_profile'),
]

