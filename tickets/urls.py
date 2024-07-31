from django.urls import path
from .views import ticket_list, ticket_detail, ticket_create, ticket_update

urlpatterns = [
    path('', ticket_list, name='ticket_list'),  # route לדף הבית
    path('<int:pk>/', ticket_detail, name='ticket_detail'),
    path('create/', ticket_create, name='ticket_create'),
    path('<int:pk>/edit/', ticket_update, name='ticket_update'),
]
