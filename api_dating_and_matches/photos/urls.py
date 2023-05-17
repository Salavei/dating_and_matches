from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from photos import views

urlpatterns = [
    path('photos/', views.PhotoListAPIView.as_view(), name='photo-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
