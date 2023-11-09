from django.urls import path
from . import views
urlpatterns = [
    path('registerPage/', views.registerPage, name='registerPage'),
    path('', views.user_login, name='login'),  # Changed to 'user_login'
    path('success/', views.success, name='success'),
]
