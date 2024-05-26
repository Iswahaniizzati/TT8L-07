from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('update_user/', view.update_user, name='update_user'),
]