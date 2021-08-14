from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list_items/', views.list_items, name='list-items'),
    path('add_items/', views.add_items, name='add-items'),
]
