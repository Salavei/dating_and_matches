from django.urls import path
from chat.views import ChatView

urlpatterns = [
    path('user/chat/<str:hash>/', ChatView.as_view(), name='chat_page'),
]