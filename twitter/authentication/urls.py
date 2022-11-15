from . import views
# from django.contrib import admin
from django.urls import path

urlpatterns = [

    path('', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('welcome', views.welcome, name='welcome'),
    path('signout', views.signout, name='signout'),

    path('adminhome', views.adminhome, name='adminhome'),
    path('adminsignin', views.adminsignin, name='adminsignin'),
    path('adminsignout', views.adminsignout, name='adminsignout'),

    path('adduser', views.adduser, name='adduser'),
    path('edituser/<int:id>', views.edituser, name='edituser'),
    path('deleteuser/<str:username>', views.deleteuser, name='deleteuser'),
    path('searchuser', views.searchuser, name='searchuser'),

]   