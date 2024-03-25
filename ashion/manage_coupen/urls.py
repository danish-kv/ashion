from django.urls import path
from . import views

urlpatterns = [
    path("coupon/", views.show_coupon, name="coupon"),
    path("add_coupon/", views.add_coupon, name="addcoupon"),
    path("edit_coupon/<str:id>", views.edit_coupon, name="editcoupon"),
    path("active_coupon/<str:id>", views.active_coupon, name="active_coupon"),
]
