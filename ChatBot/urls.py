# chatbot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),  # The main chat page
    path('get_response/', views.get_response, name='get_response'),  # Endpoint to get chatbot response
]
