from django.urls import path
from . import views

urlpatterns = [
    path('product_list/',views.product_list,name='productlist'),
    path('product_details/<str:id>/',views.product_details,name='productdetails'),
    path('search/',views.search,name='search'),
    path('add_to_whislist/<str:id>/<str:from_page>',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_from_wishlist/<str:id>',views.remove_from_wishlist,name='remove_from_wishlist')
]
