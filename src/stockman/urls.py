from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.upload, name='upload'),
    path('list_items/', views.list_items, name='list-items'),
    path('item_detail/<str:pk>/', views.stock_detail, name='stock-detail'),
    path('add_items/', views.add_items, name='add-items'),
    path('update_items/<str:pk>/', views.update_items, name='update-items'),
    path('delete_items/<str:pk>/', views.delete_items, name='delete-items'),
    path('receive_items/<str:pk>/', views.receive_item, name='receive-items'),
    path('issued_items/<str:pk>/', views.issue_items, name='issued-items'),
    path('reorder_level/<str:pk>/', views.reorder_level, name='reorder-level'),
    path('list_history/', views.list_history, name='list-history'),
]
