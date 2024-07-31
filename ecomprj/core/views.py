from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, WishList, ProductReview, Address, ProductImages
from django.db.models import Count,Avg
from taggit.models import Tag
from .forms import ProductReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

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

    # Getting all reviews for a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Average Ratings
    average_ratings = ProductReview.objects.filter(product=product).aggregate(rating = Avg("rating"))

    # Forms
    review_form = ProductReviewForm()

    p_image = product.p_images.all()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user = request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    context = {
        "product" : product,
        "make_review" : make_review,
        "p_image" : p_image,
        "average_ratings" : average_ratings,
        "reviews" : reviews,
        "products" : products,
        "review_form" : review_form,
    }
    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status = "published")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        products = products.filter(tags__in = [tag])

    context = {
        "products" : products,
        "tag" : tag,
    }
    return render(request, "core/tags.html", context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST["review"],
        rating = request.POST["rating"],
    )

    context = {
        "user" : user.username,
        "review" : request.POST["review"],
        "rating" : request.POST["rating"],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating = Avg("rating"))

    return JsonResponse(
        {
            'bool' : True,
            'context' : context,
            'average_reviews' : average_reviews
        }
    )

def search_view(request):

    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains = query).order_by("-date")

    context = {
        "products" : products,
        "query" : query,
    }
    return render(request, "core/search.html", context)

def filter_products(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    min_price = request.GET["min_price"]
    max_price = request.GET["max_price"]

    products = Product.objects.filter(product_status = "published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in = categories).distinct()

    if len(vendors) > 0:
        products= products.filter(vendor__id__in = vendors).distinct()

    data = render_to_string("core/async/product-list.html",{"products": products})

    return JsonResponse({"data": data})

def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        "title" : request.GET['title'],
        "quantity" : request.GET['quantity'],
        "price" : request.GET['price'],
        "image" : request.GET['image'],
        "pid" : request.GET['pid'],
    }

    if "cart_data_obj" in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]["quantity"] = int(cart_product[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], "totalCartItems": len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total += int(item['quantity']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], "totalCartItems": len(request.session['cart_data_obj']), "cart_total" : cart_total})
    else:
        messages.warning(request,"Cart is Empty!")
        return redirect("core:index")
    
def delete_from_cart_view(request):
    product_id = str(request.GET.get("id"))

    if "cart_data_obj" in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total += int(item['quantity']) * float(item['price'])
    
    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session['cart_data_obj'],
        "totalCartItems": len(request.session['cart_data_obj']),
        "cart_total": cart_total
    })
    
    return JsonResponse({"data": context, "totalCartItems": len(request.session['cart_data_obj'])})

def update_cart_view(request):
    product_id = str(request.GET.get("id"))
    product_quantity = request.GET['product_quantity']

    if "cart_data_obj" in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = product_quantity
            request.session['cart_data_obj'] = cart_data
    
    cart_total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total += int(item['quantity']) * float(item['price'])
    
    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session['cart_data_obj'],
        "totalCartItems": len(request.session['cart_data_obj']),
        "cart_total": cart_total
    })
    
    return JsonResponse({"data": context, "totalCartItems": len(request.session['cart_data_obj'])})