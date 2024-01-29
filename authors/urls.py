from django.urls import path
from recipes import views as recipes
from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/acess/', views.login_create, name='login_create'),
    path('', recipes.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
]
