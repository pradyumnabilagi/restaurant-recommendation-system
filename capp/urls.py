from django.urls import path
from . import views
urlpatterns = [
   
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('', views.home,name="home"),
    path('menu/<str:pk>/',views.menu1,name="menu"),
  
    path('cart/add/<int:itemid>/',views.addtocart,name="addtocart"),
    path('cart/',views.cartview,name = "cartpage"),
    path('cart/delete/<int:cartid>/',views.deletefromcart,name="delete"),
    path('placeorder/',views.placeorder,name = "placeorder"),
    path('orders/',views.ordersview,name = "orders"),
    path('search/',views.searchview,name = "search"),

]
   