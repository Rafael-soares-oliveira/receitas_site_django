from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
    path('category/<int:category_id>/', views.RecipeListViewCategory.as_view(),
         name='category'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(),
         name='search'),
]
