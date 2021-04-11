from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path('create/', views.create, name = 'create'),
    path('detail/<int:book_pk>/', views.detail, name = 'detail' ),
    path('update/<int:book_pk>/', views.update, name = 'update'),
    path('delete/<int:book_pk>/', views.delete, name = 'delete'),
]