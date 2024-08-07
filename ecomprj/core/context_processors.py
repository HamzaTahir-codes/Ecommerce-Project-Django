from .models import Product, Category, Vendor, Address, WishList
from django.db.models import Min, Max
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    if request.user.is_authenticated:
        try:
            address = Address.objects.filter(user=request.user)
        except Address.DoesNotExist:
            address = None
    else:
        address = None

    try:
        wishlist = WishList.objects.filter(user=request.user)
    except:
        messages.success(request, "you need to login first")
        wishlist = 0


    return {
        "categories": categories,
        "address": address,
        "vendors": vendors,
        "wishlist": wishlist,
        "min_max_price": min_max_price,
    }
