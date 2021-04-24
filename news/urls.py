from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('new_search', views.new_search, name='new_search')
]

