from django.urls import path
from .views import register_page, match_page, start_page, login_page, logout_page, chat_page, user_profile

urlpatterns = [
    path('', start_page, name='start_page'),
    path('register/', register_page, name='registry_page'),
    path('logout/', logout_page, name='logout_page'),
    path('match/', match_page, name='home_page'),
    path('login/', login_page, name='login_page'),
    path('chat/<str:pk>/', chat_page, name='chat_page'),
    path('profile/', user_profile, name='user_profile'),
]