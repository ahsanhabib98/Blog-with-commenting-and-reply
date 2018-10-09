from django.urls import path
from .views import post_list, post_detail


urlpatterns = [
    path('', post_list, name='list'),
    path('detail/<int:id>', post_detail, name='detail'),
]
