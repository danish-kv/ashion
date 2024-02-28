from django.urls import path
from . import views

urlpatterns = [
    path('showcart/',views.showcart,name='cart'),
    path('addtocart/<str:id>',views.add_to_cart,name='addtocart'),
    path('remove_from_cart/<str:id>',views.remove_from_cart,name="removefromcart"),
    path('update_quantity/',views.update_quantity,name='update_quantity'),
    path('checkout/',views.Checkout,name='checkout'),
    path('add_address/',views.checkout_add_address,name='add_address'),
    path('place_order/',views.place_order,name="place_order"),
    path('order_details/',views.order_details,name="order_details"),
    path('my_order/',views.my_order,name="my_order"),
    path('order_history/',views.order_history,name="order_history"),
    path('view_order/<str:id>',views.view_order,name='view_order'),
    path('order_cancel/<str:id>',views.order_cancel,name="order_cancel"),
    
]



