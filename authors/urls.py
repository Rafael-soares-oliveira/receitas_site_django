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
     path('dashboard/', views.dashboard, name='dashboard'),

     path('dashboard/recipe/<int:id>/edit/', views.dashboard_recipe_edit,
          name='dashboard_recipe_edit'),

     path('dashboard/recipe/create/', views.dashboard_recipe_create,
          name='dashboard_recipe_create'),

     path('dashboard/recipe/<int:id>/delete/', views.dashboard_recipe_delete,
          name='dashboard_recipe_delete'),

     path('dashboard/recipe/<int:id>/', views.recipe_not_published,
          name='recipe_not_published'),

     path('dashboard/recipe/<int:id>/unpublish',
          views.dashboard_recipe_unpublish,
          name='dashboard_recipe_unpublish'),
]
