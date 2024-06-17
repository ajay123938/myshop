from django.urls import path
from .  import views
from .views import custom_logout_view

urlpatterns = [
    path('cateogry/<str>',views.cateogry,name="cateogry"),
    path('login1/',views.login1,name="login1"),
    path('order/',views.order,name="order"),
    path('your_order/',views.your_order,name="your_order"),
    path('cart/',views.cart,name="cart"),
    path('register/',views.register,name="register"),
    path('logout/', custom_logout_view, name='logout'),









]