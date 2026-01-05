from django.contrib import admin
from django.urls import path
# from .views import home,signup,login
from store import views
urlpatterns = [
    path('',views.home,name='homepage'),
    path('signup',views.Signup.as_view(),name='signup'),
    path('login',views.Login.as_view(),name='login'),
    path('product-detail/<int:pk>',views.productdetail,name='product-detail'),
    path('logout',views.logout,name='logout'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('show_cart',views.show_cart,name='show_cart'),
    path('plus_cart/<int:product_id>/<str:op>/',views.plus_cart,name='plus_cart'),
    path('remove_cart/',views.remove_cart,name='remove_cart'),
    path('offers/',views.offers,name='offers'),
    path('checkout',views.checkout,name='checkout'),
    path('order',views.order,name='order'),
    path('search',views.search,name='search'),
    path('clear-orders', views.clear_orders, name='clear-orders'),
    path('about',views.about,name='about')

    
]