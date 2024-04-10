from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit/', views.profile_edit, name='edit_profile'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('dark_mode/', views.dark_mode, name='dark_mode'),
    path('search/', views.search_code, name='search'),
    


]