from django.urls import path
from . import views

urlpatterns = [
    path('adminhome/',views.AdminHome,name='adminhome'),
    path('adminlogin/',views.AdminLogin,name='adminlogin')
]
