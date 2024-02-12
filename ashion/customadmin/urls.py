from django.urls import path
from . import views

urlpatterns = [
    path('adminlogin/', views.AdminLogin, name='adminlogin'),
    path('adminhome/', views.AdminHome, name='AdminHome'),  
    path('adminlogout/',views.AdminLogout,name='adminlogout'),
    path('manageuser/',views.manage_user,name='manageuser'),
    path('blockuser/<str:id>',views.Blockuser,name='blockuser'),
    path('unblockuser/<str:id>',views.Unblockuser,name='unblockuser'),




]