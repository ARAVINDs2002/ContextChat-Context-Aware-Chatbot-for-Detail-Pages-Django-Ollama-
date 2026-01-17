from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<int:house_id>/', views.chat_view, name='chat'),
]
