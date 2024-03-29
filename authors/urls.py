from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
     path('register/', views.register_view, name='register'),
     path('register/create', views.register_create, name='register_create'),
     path('login/', views.login_view, name='login'),
     path('login/acess/', views.login_create, name='login_create'),
     path('logout/', views.logout_view, name='logout'),

     path('dashboard/', views.Dashboard.as_view(), name='dashboard'),

     path('dashboard/recipe/<int:id>/edit/',
          views.DashboardRecipeEdit.as_view(),
          name='dashboard_recipe_edit'),

     path('dashboard/recipe/create/', views.DashboardRecipeEdit.as_view(),
          name='dashboard_recipe_create'),

     path('dashboard/recipe/delete/', views.DashboardRecipeDelete.as_view(),
          name='dashboard_recipe_delete'),

     path('dashboard/recipe/<int:id>/',
          views.DashboardRecipeUnpublishView.as_view(),
          name='recipe_not_published'),

     path('dashboard/recipe/unpublish',
          views.DashboardRecipeUnpublish.as_view(),
          name='dashboard_recipe_unpublish'),

     path('profile/<int:id>/', views.ProfileView.as_view(),
          name='profile'),

     path('myprofile/', views.MyProfileView.as_view(),
          name="myprofile"),

     path('myprofile/bio_edit/', views.BioEditView.as_view(),
          name="myprofile_bio_edit"),

     path('myprofile/edit/', views.MyProfileEditView.as_view(),
          name="myprofile_edit"),

     path('myprofile/edit/password/',
          views.PasswordsChangeView.as_view(),
          name='myprofile_edit_password'),

     path('myprofile/edit/password/done/',
          views.PasswordsDoneChangeView.as_view(),
          name='myprofile_edit_password_done'),
]
