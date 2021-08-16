from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list_items/', views.list_items, name='list-items'),
    path('item_detail/<str:pk>/', views.stock_detail, name='stock-detail'),
    path('add_items/', views.add_items, name='add-items'),
    path('update_items/<str:pk>/', views.update_items, name='update-items'),
    path('delete_items/<str:pk>/', views.delete_items, name='delete-items'),
]
