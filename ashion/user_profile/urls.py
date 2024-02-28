from django.urls import path
from . import views

urlpatterns = [
    path('user_dashbord/',views.user_profile,name='user_profile'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('edit_address/<str:id>',views.edit_address, name='edit_address'),
    path('delete_address/<str:id>',views.delete_address,name='delete_address')
]

