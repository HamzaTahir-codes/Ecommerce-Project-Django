from django.urls import path, include
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

    #CheckOut!
    path("checkout/<oid>/", views.checkout_view, name="checkout"),
    

    #Paypal
    path("paypal/", include('paypal.standard.ipn.urls'), name="paypal-ipn"),
    path("payment-successfull/", views.payment_successfull, name="payment-successfull"),
    path("payment-failed/", views.payment_failed, name="payment-failed"),

    #Dashboard
    path("dashboard/", views.customer_dashboard, name="dashboard"),

    #order detail
    path("dashboard/order/<int:id>/", views.order_products, name="order-detail"),

    #Make Default
    path("make-default-address/", views.make_default_address, name="make-default-address"),

    #Wishlist
    path("wishlist/", views.wishlist_view, name="wishlist"),

    #Add to wishlist
    path("add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),

    #Remove from wishlist
    path("remove-from-wishlist/", views.remove_from_wishlist, name="remove-from-wishlist"),

    #Contact US
    path("contact-us/", views.contact_us, name="contact"),
    path("ajax-contact-us", views.ajax_contact_us, name="ajax_contact_us"),

    #new paths
    path("save-checkout-info/", views.save_checkout_info, name="save-checkout-info"),
    ]