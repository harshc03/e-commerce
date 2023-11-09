from django.urls import path
from . import views
urlpatterns = [
    path('product-page/<int:product_id>/', views.product_detail, name='product_page'),
    path('product-list/', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout_view'),
]
