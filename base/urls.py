from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('register/', views.register_page, name='registry_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('match/', views.match_page, name='home_page'),
    path('login/', views.login_page, name='login_page'),
    path('chat/<str:hash>/', views.chat_page, name='chat_page'),
    path('profile/', views.user_profile, name='user_profile'),
]