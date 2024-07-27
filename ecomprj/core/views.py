from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, WishList, ProductReview, Address, ProductImages
from django.db.models import Count,Avg
from taggit.models import Tag
from .forms import ProductReviewForm
from django.http import JsonResponse

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

    context = {
        "product" : product,
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
        "review" : {
            "review" : review.review,
            "rating" : review.rating,
        },
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating = Avg("rating"))

    return JsonResponse(
        {
            'bool' : True,
            'context' : context,
            'average_reviews' : average_reviews
        }
    )
