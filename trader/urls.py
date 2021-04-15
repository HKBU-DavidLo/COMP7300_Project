from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('buy/', views.buy, name='buy'),
    #path('buy-order/', views.buyorder, name='buy-order'),
    path('order-preview/', views.orderpreview, name='order-preview'),
    path('signout/', views.signout, name='signout'),
    path('getquote/', views.getquote, name='getquote'),
    path('confirm-buy/', views.confirmbuy, name='confirm-buy'),
]