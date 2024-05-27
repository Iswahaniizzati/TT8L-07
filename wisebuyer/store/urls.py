from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('update_user/', views.update_user, name='update_user'),
     path('about/', views.about, name='about'),
]