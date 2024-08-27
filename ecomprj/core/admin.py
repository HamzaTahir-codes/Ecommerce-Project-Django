from django.contrib import admin
from .models import Coupon, Product, Category, Vendor, CartOrder, CartOrderItems, WishList, ProductReview, Address, ProductImages
# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_editable = ['deal_of_the_day', 'featured']
    list_display = ['user', 'title', 'category', 'vendor', 'product_image', 'price', 'featured', 'product_status', 'deal_of_the_day']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category_image"]

class VendorAdmin(admin.ModelAdmin):
    list_display = ["title", "vendor_image"]

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ["paid_status", "product_status"]
    list_display = ["user", "price", "paid_status", "order_date", "product_status"]

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "invoice_no", "item", "image", "qty", "price", "total"]
 
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "review", "rating"]

class WishListAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]

class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "discount", "active"]

class AddressAdmin(admin.ModelAdmin):
    list_editable = ["address", "status"]
    list_display = ["user", "address", "status", "phone", "city", "state"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Address, AddressAdmin) 
admin.site.register(Coupon, CouponAdmin) 