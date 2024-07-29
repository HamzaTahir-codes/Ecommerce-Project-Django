from .models import Product, Category, Vendor, CartOrder, CartOrderItems, WishList, ProductReview, Address, ProductImages

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    try:
        address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        address = None

    return {
        "categories" : categories,
        "address" : address,
        "vendors" : vendors,
    }