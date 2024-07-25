from .models import Product, Category, Vendor, CartOrder, CartOrderItems, WishList, ProductReview, Address, ProductImages

def default(request):
    categories = Category.objects.all()
    address = Address.objects.get(user=request.user)

    return {
        "categories" : categories,
        "address" : address,
    }