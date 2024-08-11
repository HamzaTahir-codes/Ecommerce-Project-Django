from django.urls import path
from . import views

app_name = "useradmin"

urlpatterns = [
    path("dashboard/", views.dashboard, name="vendor-dashboard"),
    path("products/", views.products, name="products"),
    path("add-product/", views.add_product, name="add-product"),
    path("edit-product/<pid>/", views.edit_product, name="edit-product"),
    path("delete-product/<pid>/", views.delete_product, name="delete-product"),
    path("orders-list/", views.orders_list, name="orders-list"),
    path("order-detail/<oid>/", views.orders_detail, name="order-detail"),
    path("change-product-status/<oid>/", views.change_product_status, name="change-product-status"),
    path("shop-page/", views.shop_page, name="shop-page"),
    path("reviews/", views.reviews, name="reviews"),
    path("settings/", views.settings, name="settings"),
    path("change-password/", views.change_password, name="change-password"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]
