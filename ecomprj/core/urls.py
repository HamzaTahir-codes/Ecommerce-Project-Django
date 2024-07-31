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

    #Tags
    path("product/tags/<slug:tag_slug>/",views.tag_list, name="tag-list"),

    #Review
    path("ajax-add-review/<int:pid>/", views.ajax_add_review, name="ajax-add-review"),

    # SEARCH
    path("search/", views.search_view, name="search"),

    # Filter
    path("filter-products/", views.filter_products, name="filter-products"),

    #Add to Cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    #Cart List
    path("cart/", views.cart_view, name="cart"),
    #Delete from Cart
    path("delete-from-cart/", views.delete_from_cart_view, name="delete-from-cart"),
    #Update cart view
    path("update-cart/", views.update_cart_view, name="update-cart"),
    ]