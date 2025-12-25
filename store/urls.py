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
    path('show_cart',views.show_cart,name='show_cart')
]