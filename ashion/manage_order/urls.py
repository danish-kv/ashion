from django.urls import path
from . import views

urlpatterns = [
    path('manage_order/',views.manage_order,name='manage_order'),
    path('order_details_view/<str:id>',views.order_details_view,name='order_deatils_view'),
    path('change_order_status/<str:id>',views.change_order_status,name='change_order_status'),
    path('cancel_request/',views.cancel_request,name='cancel_request')
    
]

