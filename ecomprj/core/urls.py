from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # HOMEPAGE
    path('', views.index, name="index"),
    path("products/", views.product_list, name="product-list"),
    path("product/<pid>/", views.product_detail, name="product-detail"),

    # CATEGORY VIEW
    path("category/", views.category_list, name="category-list"),
    path("category/<cid>/", views.category_product_list, name="category-product-list"),

    # VENDOR VIEW
    path("vendors/", views.vendor_list, name="vendor-list"),
    path("vendor/<vid>/", views.vendor_detail, name="vendor-detail"),
    ]
