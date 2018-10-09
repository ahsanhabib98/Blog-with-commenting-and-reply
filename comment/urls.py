from django.urls import path
from .views import comment_thread


urlpatterns = [
    path('thread/<int:id>', comment_thread, name='thread'),
]
