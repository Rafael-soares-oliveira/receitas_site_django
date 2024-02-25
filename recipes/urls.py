from django.urls import path
from .views import views_site, views_api

app_name = 'recipes'

urlpatterns = [
     # Recipe
     path('', views_site.RecipeListViewHome.as_view(), name='home'),
     path('recipes/<int:pk>/', views_site.RecipeDetail.as_view(),
          name='recipe'),
     path('category/<int:category_id>/',
          views_site.RecipeListViewCategory.as_view(), name='category'),
     path('recipes/search/', views_site.RecipeListViewSearch.as_view(),
          name='search'),
     path('recipes/api/v1/', views_site.RecipeListViewHomeApi.as_view(),
          name='recipes_api_v1',
          ),
     path('recipes/api/v1/<int:pk>/', views_site.RecipeDetailAPI.as_view(),
          name='recipes_detail_api_v1',
          ),
     path('recipes/tags/<slug:slug>/', views_site.RecipeListViewTag.as_view(),
          name='tag'),

     # Toggle menu
     path('menu/', views_site.menu, name='menu'),

     # API View
     path('recipes/api/v2/', views_api.recipe_api_list,
          name='recipes_api_v2'),
     path('recipes/api/v2/<int:pk>/', views_api.recipe_api_detail,
          name='recipes_api_v2_detail'),
     path('recipes/api/v2/tag/<int:pk>/', views_api.recipe_api_tag,
          name='recipes_api_v2_tag'),
]
