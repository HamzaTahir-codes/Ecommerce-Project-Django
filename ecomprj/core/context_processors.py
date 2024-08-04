from .models import Product, Category, Vendor, Address
from django.db.models import Min, Max
from django.contrib.auth.models import AnonymousUser

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

    return {
        "categories": categories,
        "address": address,
        "vendors": vendors,
        "min_max_price": min_max_price,
    }
