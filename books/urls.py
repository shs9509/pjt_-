from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('genre/<str:book_genre>/', views.genre, name = 'genre'),
    path('create/', views.create, name = 'create'),
    path('detail/<int:pk>/', views.detail, name = 'detail' ),
    path('update/<int:pk>/', views.update, name = 'update'),
    path('delete/<int:pk>/', views.delete, name = 'delete'),
    path('<int:pk>/comment', views.comments_create, name='comments_create'),
    path('<int:book_pk>/like',views.likes, name='likes'),
]