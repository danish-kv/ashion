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
    path('my_order/',views.my_order,name="my_order"),
    path('ordered_products/<str:id>',views.ordered_products,name="ordered_products"),
    path('order_success/<str:id>',views.order_success,name='order_success'),
    path('order_cancel/<str:id>',views.order_cancel,name="order_cancel"),
    path('return_order/<str:id>',views.return_order,name='return_order'),
    path('razorpay_payment/',views.razorpay_payment,name='razor_pay'),
    path('apply_coupon/',views.apply_coupon, name='apply_coupon'),
    path('remove_coupen/<str:id>', views.remove_coupen, name='remove_coupen'),
    
]



