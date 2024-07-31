from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('create/', views.ticket_create, name='ticket_create'),
    path('<int:pk>/edit/', views.ticket_update, name='ticket_update'),
]
