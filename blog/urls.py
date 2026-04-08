from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('add/', views.add_article, name='add_article'),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
]