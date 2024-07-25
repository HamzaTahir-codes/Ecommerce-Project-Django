from django.shortcuts import render
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, WishList, ProductReview, Address, ProductImages
from django.db.models import Count

def index(request):
    # product = Product.objects.all().order_by("-id")
    product = Product.objects.filter(product_status = "published", featured = True)
    context = {
        "product" : product,
    }
    return render(request, 'core/index.html', context)

def product_list(request):
    product = Product.objects.filter(product_status = "published")
    context = {
        "products" : product,
    }
    return render(request, 'core/product-list.html', context)

def category_list(request):
    categories = Category.objects.all()
    # categories = Category.objects.all().annotate(product_count = Count("products"))
    context = {
        "categories" : categories,
    }
    return render(request, "core/category-list.html", context)

def category_product_list(request, cid):
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(product_status = "published", category = category)

    context = {
        "category" : category,
        "products" : products,
    }
    return render(request, "core/category-product-list.html", context)

def vendor_list(request):
    vendors = Vendor.objects.all()

    context = {
        "vendors" : vendors,
    }
    return render(request, "core/vendor-list.html", context)

def vendor_detail(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status = "published", vendor=vendor)
    context = {
        "vendor" : vendor,
        "products" : products,
    }
    return render(request, "core/vendor-detail.html", context)

def product_detail(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category = product.category).exclude(pid=pid)
    p_image = product.p_images.all()

    context = {
        "product" : product,
        "p_image" : p_image,
        "products" : products,
    }
    return render(request, "core/product-detail.html", context)