from django.urls import path
from . import views

urlpatterns = [
    path('manage_order/',views.manage_order,name='manage_order'),
    path('order_details_view/<str:id>',views.order_details_view,name='order_deatils_view'),
    path('change_order_status/<str:id>',views.change_order_status,name='change_order_status'),
    path('cancelled_orders/',views.cancelled_orders,name='cancelled_orders'),
    path('order_return/',views.order_return,name='order_return')
]

