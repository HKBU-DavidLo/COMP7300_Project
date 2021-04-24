from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('buyorder-preview/', views.buyorderpreview, name='buyorder-preview'),
    path('sellorder-preview/', views.sellorderpreview, name='sellorder-preview'),
    path('signout/', views.signout, name='signout'),
    path('getquote/', views.getquote, name='getquote'),
    path('confirm-buy/', views.confirmbuy, name='confirm-buy'),
    path('confirm-sell/', views.confirmsell, name='confirm-sell'),
    path('deposit-cash/', views.depositcash, name='deposit-cash'),
    path('withdraw-cash/', views.withdrawcash, name='withdraw-cash'),
    path('deposit-preview/', views.depositpreview, name='deposit-preview'),
    path('withdraw-preview/', views.withdrawpreview, name='withdraw-preview'),
    path('confirm-deposit/', views.confirmdeposit, name='confirm-deposit'),
    path('prediction/', views.prediction, name='prediction'),
    path('confirm-withdraw/', views.confirmwithdraw, name='confirm-withdraw'),
    path('testai/', views.testai, name="testai"),
    path('getprediction/', views.getprediction, name='getprediction'),
]