from django.urls import path
from . import views

urlpatterns = [
    path("adminlogin/", views.AdminLogin, name="adminlogin"),
    path("adminhome/", views.AdminHome, name="AdminHome"),
    path("adminlogout/", views.AdminLogout, name="adminlogout"),
    path("manageuser/", views.manage_user, name="manageuser"),
    path("blockuser/<str:id>", views.Blockuser, name="blockuser"),
    path("unblockuser/<str:id>", views.Unblockuser, name="unblockuser"),
    path("product_offers/", views.product_offers, name="product_offers"),
    path("add_product_offers/", views.add_product_offers, name="add_product_offers"),
    path(
        "edit_product_offers/<str:id>",
        views.edit_product_offers,
        name="edit_product_offers",
    ),
    path(
        "product_offer_status/<str:id>",
        views.product_offer_status,
        name="product_offer_status",
    ),
    path("category_offers/", views.category_offers, name="category_offers"),
    path("add_category_offers/", views.add_category_offers, name="add_category_offers"),
    path(
        "edit_category_offers/<str:id>",
        views.edit_category_offers,
        name="edit_category_offers",
    ),
    path(
        "category_offer_status/<str:id>",
        views.category_offer_status,
        name="category_offer_status",
    ),
    path("sales_report/", views.sales_report, name="sales_report"),
]
