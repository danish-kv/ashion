from django.urls import path
from . import views

urlpatterns = [
    path("product/", views.product, name="product"),
    path("addproduct/", views.addproduct, name="addproduct"),
    path("editproduct/<str:id>", views.editproduct, name="editproduct"),
    path("list_product/<str:id>", views.list_product, name="listproduct"),
    path("unlist_product/<str:id>", views.unlist_product, name="unlistproduct"),
    path("variant/<str:id>", views.Show_variant, name="show_variant"),
    path("add_variant/<str:id>", views.Add_variant, name="add_variant"),
    path("edit_variant/<str:id>", views.Edit_variant, name="edit_variant"),
]
