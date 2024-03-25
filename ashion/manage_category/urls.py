from django.urls import path
from . import views

urlpatterns = [
    path("category/", views.category_view, name="category"),
    path("addcategory/", views.add_category_view, name="addcategory"),
    path("edit_category/<str:id>", views.edit_category_view, name="editcategory"),
    path("listcategory/<str:id>", views.list_category, name="listcategory"),
    path("unlistcategory/<str:id>", views.unlist_category, name="unlistcategory"),
]
